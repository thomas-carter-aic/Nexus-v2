"""
Enterprise Encryption Service

This module provides comprehensive encryption capabilities including data at rest,
data in transit, key management, and cryptographic operations for the AI-Native PaaS Platform.
"""

import asyncio
import base64
import hashlib
import secrets
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

logger = logging.getLogger(__name__)


class EncryptionAlgorithm(Enum):
    """Supported encryption algorithms"""
    AES_256_GCM = "aes_256_gcm"
    AES_256_CBC = "aes_256_cbc"
    CHACHA20_POLY1305 = "chacha20_poly1305"
    RSA_2048 = "rsa_2048"
    RSA_4096 = "rsa_4096"
    FERNET = "fernet"


class KeyType(Enum):
    """Types of encryption keys"""
    SYMMETRIC = "symmetric"
    ASYMMETRIC_PUBLIC = "asymmetric_public"
    ASYMMETRIC_PRIVATE = "asymmetric_private"
    MASTER_KEY = "master_key"
    DATA_ENCRYPTION_KEY = "data_encryption_key"


class KeyStatus(Enum):
    """Key lifecycle status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPROMISED = "compromised"
    EXPIRED = "expired"
    PENDING_DELETION = "pending_deletion"


@dataclass
class EncryptionKey:
    """Encryption key metadata and material"""
    key_id: str
    key_type: KeyType
    algorithm: EncryptionAlgorithm
    key_material: bytes
    status: KeyStatus = KeyStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    usage_count: int = 0
    max_usage: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self, include_key_material: bool = False) -> Dict[str, Any]:
        result = {
            'key_id': self.key_id,
            'key_type': self.key_type.value,
            'algorithm': self.algorithm.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'usage_count': self.usage_count,
            'max_usage': self.max_usage,
            'metadata': self.metadata
        }
        
        if include_key_material:
            result['key_material'] = base64.b64encode(self.key_material).decode('utf-8')
            
        return result


@dataclass
class EncryptionResult:
    """Result of encryption operation"""
    encrypted_data: bytes
    key_id: str
    algorithm: EncryptionAlgorithm
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'encrypted_data': base64.b64encode(self.encrypted_data).decode('utf-8'),
            'key_id': self.key_id,
            'algorithm': self.algorithm.value,
            'iv': base64.b64encode(self.iv).decode('utf-8') if self.iv else None,
            'tag': base64.b64encode(self.tag).decode('utf-8') if self.tag else None,
            'metadata': self.metadata
        }


class KeyManager:
    """
    Secure key management system with key rotation and lifecycle management
    """
    
    def __init__(self):
        self.keys: Dict[str, EncryptionKey] = {}
        self.key_hierarchy: Dict[str, List[str]] = {}  # Master key -> DEKs
        self.rotation_policies: Dict[str, Dict[str, Any]] = {}
        
    async def generate_key(self, algorithm: EncryptionAlgorithm, 
                          key_type: KeyType,
                          expires_in_days: Optional[int] = None,
                          metadata: Optional[Dict[str, Any]] = None) -> str:
        """Generate a new encryption key"""
        
        key_id = str(uuid4())
        
        # Generate key material based on algorithm
        if algorithm == EncryptionAlgorithm.AES_256_GCM:
            key_material = os.urandom(32)  # 256 bits
        elif algorithm == EncryptionAlgorithm.AES_256_CBC:
            key_material = os.urandom(32)  # 256 bits
        elif algorithm == EncryptionAlgorithm.CHACHA20_POLY1305:
            key_material = os.urandom(32)  # 256 bits
        elif algorithm == EncryptionAlgorithm.FERNET:
            key_material = Fernet.generate_key()
        elif algorithm in [EncryptionAlgorithm.RSA_2048, EncryptionAlgorithm.RSA_4096]:
            key_size = 2048 if algorithm == EncryptionAlgorithm.RSA_2048 else 4096
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend()
            )
            
            if key_type == KeyType.ASYMMETRIC_PRIVATE:
                key_material = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            else:  # Public key
                public_key = private_key.public_key()
                key_material = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
            
        # Set expiration
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
            
        # Create key object
        key = EncryptionKey(
            key_id=key_id,
            key_type=key_type,
            algorithm=algorithm,
            key_material=key_material,
            expires_at=expires_at,
            metadata=metadata or {}
        )
        
        self.keys[key_id] = key
        
        logger.info(f"Generated {algorithm.value} key: {key_id}")
        return key_id
        
    async def get_key(self, key_id: str) -> Optional[EncryptionKey]:
        """Retrieve encryption key by ID"""
        key = self.keys.get(key_id)
        
        if key and key.status == KeyStatus.ACTIVE:
            # Check expiration
            if key.expires_at and datetime.utcnow() > key.expires_at:
                key.status = KeyStatus.EXPIRED
                logger.warning(f"Key {key_id} has expired")
                return None
                
            # Check usage limits
            if key.max_usage and key.usage_count >= key.max_usage:
                key.status = KeyStatus.INACTIVE
                logger.warning(f"Key {key_id} has reached usage limit")
                return None
                
            return key
            
        return None
        
    async def rotate_key(self, key_id: str) -> str:
        """Rotate an encryption key"""
        old_key = self.keys.get(key_id)
        if not old_key:
            raise ValueError(f"Key {key_id} not found")
            
        # Generate new key with same parameters
        new_key_id = await self.generate_key(
            algorithm=old_key.algorithm,
            key_type=old_key.key_type,
            expires_in_days=365,  # Default 1 year
            metadata=old_key.metadata.copy()
        )
        
        # Mark old key as inactive
        old_key.status = KeyStatus.INACTIVE
        
        # Update key hierarchy if applicable
        if key_id in self.key_hierarchy:
            self.key_hierarchy[new_key_id] = self.key_hierarchy.pop(key_id)
            
        logger.info(f"Rotated key {key_id} -> {new_key_id}")
        return new_key_id
        
    async def revoke_key(self, key_id: str, reason: str = "Manual revocation") -> bool:
        """Revoke an encryption key"""
        key = self.keys.get(key_id)
        if not key:
            return False
            
        key.status = KeyStatus.COMPROMISED
        key.metadata['revocation_reason'] = reason
        key.metadata['revoked_at'] = datetime.utcnow().isoformat()
        
        logger.warning(f"Revoked key {key_id}: {reason}")
        return True
        
    async def list_keys(self, status: Optional[KeyStatus] = None,
                       algorithm: Optional[EncryptionAlgorithm] = None) -> List[EncryptionKey]:
        """List encryption keys with optional filtering"""
        keys = list(self.keys.values())
        
        if status:
            keys = [k for k in keys if k.status == status]
            
        if algorithm:
            keys = [k for k in keys if k.algorithm == algorithm]
            
        return keys
        
    async def cleanup_expired_keys(self) -> int:
        """Clean up expired and revoked keys"""
        cleanup_count = 0
        current_time = datetime.utcnow()
        
        for key_id, key in list(self.keys.items()):
            should_delete = False
            
            # Delete keys marked for deletion after grace period
            if key.status == KeyStatus.PENDING_DELETION:
                deletion_time = key.metadata.get('deletion_scheduled')
                if deletion_time and current_time > datetime.fromisoformat(deletion_time):
                    should_delete = True
                    
            # Mark expired keys for deletion
            elif key.expires_at and current_time > key.expires_at + timedelta(days=30):
                key.status = KeyStatus.PENDING_DELETION
                key.metadata['deletion_scheduled'] = (current_time + timedelta(days=7)).isoformat()
                
            if should_delete:
                del self.keys[key_id]
                cleanup_count += 1
                logger.info(f"Deleted expired key: {key_id}")
                
        return cleanup_count


class EncryptionService:
    """
    Comprehensive encryption service with multiple algorithms and key management
    """
    
    def __init__(self):
        self.key_manager = KeyManager()
        self.encryption_stats: Dict[str, int] = {
            'encryptions': 0,
            'decryptions': 0,
            'key_generations': 0,
            'key_rotations': 0
        }
        
    async def encrypt_data(self, data: Union[str, bytes], 
                          key_id: Optional[str] = None,
                          algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256_GCM,
                          additional_data: Optional[bytes] = None) -> EncryptionResult:
        """Encrypt data using specified algorithm and key"""
        
        # Convert string to bytes if necessary
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        # Get or generate key
        if key_id:
            key = await self.key_manager.get_key(key_id)
            if not key:
                raise ValueError(f"Key {key_id} not found or inactive")
        else:
            # Generate new key
            key_type = KeyType.SYMMETRIC if algorithm != EncryptionAlgorithm.RSA_2048 else KeyType.ASYMMETRIC_PUBLIC
            key_id = await self.key_manager.generate_key(algorithm, key_type)
            key = await self.key_manager.get_key(key_id)
            
        # Perform encryption based on algorithm
        if algorithm == EncryptionAlgorithm.AES_256_GCM:
            result = await self._encrypt_aes_gcm(data, key, additional_data)
        elif algorithm == EncryptionAlgorithm.AES_256_CBC:
            result = await self._encrypt_aes_cbc(data, key)
        elif algorithm == EncryptionAlgorithm.CHACHA20_POLY1305:
            result = await self._encrypt_chacha20(data, key, additional_data)
        elif algorithm == EncryptionAlgorithm.FERNET:
            result = await self._encrypt_fernet(data, key)
        elif algorithm in [EncryptionAlgorithm.RSA_2048, EncryptionAlgorithm.RSA_4096]:
            result = await self._encrypt_rsa(data, key)
        else:
            raise ValueError(f"Unsupported encryption algorithm: {algorithm}")
            
        # Update key usage
        key.usage_count += 1
        self.encryption_stats['encryptions'] += 1
        
        return result
        
    async def decrypt_data(self, encrypted_result: Union[EncryptionResult, Dict[str, Any]],
                          additional_data: Optional[bytes] = None) -> bytes:
        """Decrypt data using the encryption result metadata"""
        
        # Handle dict input
        if isinstance(encrypted_result, dict):
            encrypted_data = base64.b64decode(encrypted_result['encrypted_data'])
            key_id = encrypted_result['key_id']
            algorithm = EncryptionAlgorithm(encrypted_result['algorithm'])
            iv = base64.b64decode(encrypted_result['iv']) if encrypted_result.get('iv') else None
            tag = base64.b64decode(encrypted_result['tag']) if encrypted_result.get('tag') else None
            
            encrypted_result = EncryptionResult(
                encrypted_data=encrypted_data,
                key_id=key_id,
                algorithm=algorithm,
                iv=iv,
                tag=tag
            )
            
        # Get decryption key
        key = await self.key_manager.get_key(encrypted_result.key_id)
        if not key:
            raise ValueError(f"Decryption key {encrypted_result.key_id} not found or inactive")
            
        # Perform decryption based on algorithm
        if encrypted_result.algorithm == EncryptionAlgorithm.AES_256_GCM:
            data = await self._decrypt_aes_gcm(encrypted_result, key, additional_data)
        elif encrypted_result.algorithm == EncryptionAlgorithm.AES_256_CBC:
            data = await self._decrypt_aes_cbc(encrypted_result, key)
        elif encrypted_result.algorithm == EncryptionAlgorithm.CHACHA20_POLY1305:
            data = await self._decrypt_chacha20(encrypted_result, key, additional_data)
        elif encrypted_result.algorithm == EncryptionAlgorithm.FERNET:
            data = await self._decrypt_fernet(encrypted_result, key)
        elif encrypted_result.algorithm in [EncryptionAlgorithm.RSA_2048, EncryptionAlgorithm.RSA_4096]:
            data = await self._decrypt_rsa(encrypted_result, key)
        else:
            raise ValueError(f"Unsupported decryption algorithm: {encrypted_result.algorithm}")
            
        # Update statistics
        key.usage_count += 1
        self.encryption_stats['decryptions'] += 1
        
        return data
        
    async def _encrypt_aes_gcm(self, data: bytes, key: EncryptionKey, 
                             additional_data: Optional[bytes] = None) -> EncryptionResult:
        """Encrypt using AES-256-GCM"""
        iv = os.urandom(12)  # 96-bit IV for GCM
        
        cipher = Cipher(
            algorithms.AES(key.key_material),
            modes.GCM(iv),
            backend=default_backend()
        )
        
        encryptor = cipher.encryptor()
        
        if additional_data:
            encryptor.authenticate_additional_data(additional_data)
            
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        
        return EncryptionResult(
            encrypted_data=encrypted_data,
            key_id=key.key_id,
            algorithm=EncryptionAlgorithm.AES_256_GCM,
            iv=iv,
            tag=encryptor.tag
        )
        
    async def _decrypt_aes_gcm(self, encrypted_result: EncryptionResult, 
                             key: EncryptionKey,
                             additional_data: Optional[bytes] = None) -> bytes:
        """Decrypt using AES-256-GCM"""
        cipher = Cipher(
            algorithms.AES(key.key_material),
            modes.GCM(encrypted_result.iv, encrypted_result.tag),
            backend=default_backend()
        )
        
        decryptor = cipher.decryptor()
        
        if additional_data:
            decryptor.authenticate_additional_data(additional_data)
            
        return decryptor.update(encrypted_result.encrypted_data) + decryptor.finalize()
        
    async def _encrypt_aes_cbc(self, data: bytes, key: EncryptionKey) -> EncryptionResult:
        """Encrypt using AES-256-CBC"""
        iv = os.urandom(16)  # 128-bit IV for CBC
        
        # Pad data to block size
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_length] * padding_length)
        
        cipher = Cipher(
            algorithms.AES(key.key_material),
            modes.CBC(iv),
            backend=default_backend()
        )
        
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        return EncryptionResult(
            encrypted_data=encrypted_data,
            key_id=key.key_id,
            algorithm=EncryptionAlgorithm.AES_256_CBC,
            iv=iv
        )
        
    async def _decrypt_aes_cbc(self, encrypted_result: EncryptionResult, 
                             key: EncryptionKey) -> bytes:
        """Decrypt using AES-256-CBC"""
        cipher = Cipher(
            algorithms.AES(key.key_material),
            modes.CBC(encrypted_result.iv),
            backend=default_backend()
        )
        
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_result.encrypted_data) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]
        
    async def _encrypt_chacha20(self, data: bytes, key: EncryptionKey,
                              additional_data: Optional[bytes] = None) -> EncryptionResult:
        """Encrypt using ChaCha20-Poly1305"""
        nonce = os.urandom(12)  # 96-bit nonce
        
        cipher = Cipher(
            algorithms.ChaCha20(key.key_material, nonce),
            modes.GCM(b'\x00' * 12),  # ChaCha20-Poly1305 uses internal authentication
            backend=default_backend()
        )
        
        encryptor = cipher.encryptor()
        
        if additional_data:
            encryptor.authenticate_additional_data(additional_data)
            
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        
        return EncryptionResult(
            encrypted_data=encrypted_data,
            key_id=key.key_id,
            algorithm=EncryptionAlgorithm.CHACHA20_POLY1305,
            iv=nonce,
            tag=encryptor.tag
        )
        
    async def _decrypt_chacha20(self, encrypted_result: EncryptionResult,
                              key: EncryptionKey,
                              additional_data: Optional[bytes] = None) -> bytes:
        """Decrypt using ChaCha20-Poly1305"""
        cipher = Cipher(
            algorithms.ChaCha20(key.key_material, encrypted_result.iv),
            modes.GCM(b'\x00' * 12, encrypted_result.tag),
            backend=default_backend()
        )
        
        decryptor = cipher.decryptor()
        
        if additional_data:
            decryptor.authenticate_additional_data(additional_data)
            
        return decryptor.update(encrypted_result.encrypted_data) + decryptor.finalize()
        
    async def _encrypt_fernet(self, data: bytes, key: EncryptionKey) -> EncryptionResult:
        """Encrypt using Fernet (symmetric encryption)"""
        fernet = Fernet(key.key_material)
        encrypted_data = fernet.encrypt(data)
        
        return EncryptionResult(
            encrypted_data=encrypted_data,
            key_id=key.key_id,
            algorithm=EncryptionAlgorithm.FERNET
        )
        
    async def _decrypt_fernet(self, encrypted_result: EncryptionResult,
                            key: EncryptionKey) -> bytes:
        """Decrypt using Fernet"""
        fernet = Fernet(key.key_material)
        return fernet.decrypt(encrypted_result.encrypted_data)
        
    async def _encrypt_rsa(self, data: bytes, key: EncryptionKey) -> EncryptionResult:
        """Encrypt using RSA"""
        public_key = serialization.load_pem_public_key(
            key.key_material,
            backend=default_backend()
        )
        
        encrypted_data = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return EncryptionResult(
            encrypted_data=encrypted_data,
            key_id=key.key_id,
            algorithm=key.algorithm
        )
        
    async def _decrypt_rsa(self, encrypted_result: EncryptionResult,
                         key: EncryptionKey) -> bytes:
        """Decrypt using RSA"""
        private_key = serialization.load_pem_private_key(
            key.key_material,
            password=None,
            backend=default_backend()
        )
        
        return private_key.decrypt(
            encrypted_result.encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
    async def hash_data(self, data: Union[str, bytes], 
                       algorithm: str = 'sha256') -> str:
        """Hash data using specified algorithm"""
        if isinstance(data, str):
            data = data.encode('utf-8')
            
        if algorithm == 'sha256':
            hash_obj = hashlib.sha256(data)
        elif algorithm == 'sha512':
            hash_obj = hashlib.sha512(data)
        elif algorithm == 'blake2b':
            hash_obj = hashlib.blake2b(data)
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
            
        return hash_obj.hexdigest()
        
    async def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure random token"""
        return secrets.token_urlsafe(length)
        
    async def derive_key(self, password: str, salt: Optional[bytes] = None,
                        iterations: int = 100000) -> Tuple[bytes, bytes]:
        """Derive encryption key from password using PBKDF2"""
        if salt is None:
            salt = os.urandom(16)
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        
        key = kdf.derive(password.encode('utf-8'))
        return key, salt
        
    async def get_encryption_stats(self) -> Dict[str, Any]:
        """Get encryption service statistics"""
        active_keys = len([k for k in self.key_manager.keys.values() if k.status == KeyStatus.ACTIVE])
        
        return {
            'total_keys': len(self.key_manager.keys),
            'active_keys': active_keys,
            'encryptions_performed': self.encryption_stats['encryptions'],
            'decryptions_performed': self.encryption_stats['decryptions'],
            'keys_generated': self.encryption_stats['key_generations'],
            'keys_rotated': self.encryption_stats['key_rotations'],
            'algorithms_supported': [alg.value for alg in EncryptionAlgorithm]
        }


# Example usage
async def example_encryption_service():
    """Example of using the encryption service"""
    
    # Create encryption service
    encryption_service = EncryptionService()
    
    # Encrypt sensitive data
    sensitive_data = "This is highly confidential information"
    
    # Encrypt with AES-256-GCM
    encrypted_result = await encryption_service.encrypt_data(
        sensitive_data,
        algorithm=EncryptionAlgorithm.AES_256_GCM
    )
    
    print(f"Encrypted data with key: {encrypted_result.key_id}")
    
    # Decrypt the data
    decrypted_data = await encryption_service.decrypt_data(encrypted_result)
    print(f"Decrypted: {decrypted_data.decode('utf-8')}")
    
    # Generate RSA key pair
    private_key_id = await encryption_service.key_manager.generate_key(
        EncryptionAlgorithm.RSA_2048,
        KeyType.ASYMMETRIC_PRIVATE
    )
    
    # Hash data
    data_hash = await encryption_service.hash_data(sensitive_data)
    print(f"SHA-256 hash: {data_hash}")
    
    # Generate secure token
    token = await encryption_service.generate_secure_token()
    print(f"Secure token: {token}")
    
    # Get encryption statistics
    stats = await encryption_service.get_encryption_stats()
    print(f"Encryption stats: {stats}")


if __name__ == "__main__":
    asyncio.run(example_encryption_service())
