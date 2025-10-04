import { writeFile, mkdir, access } from 'fs/promises';
import { constants } from 'fs';
import path from 'path';
import { NextRequest } from 'next/server';

export interface FileUploadConfig {
  maxSize: number;
  allowedTypes: string[];
  uploadDir: string;
}

export interface UploadedFile {
  filename: string;
  originalName: string;
  path: string;
  size: number;
  mimetype: string;
  url: string;
}

export class FileStorageService {
  private config: FileUploadConfig;

  constructor(config?: Partial<FileUploadConfig>) {
    this.config = {
      maxSize: parseInt(process.env.MAX_FILE_SIZE || '5242880'), // 5MB default
      allowedTypes: (process.env.ALLOWED_FILE_TYPES || 'application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document').split(','),
      uploadDir: process.env.UPLOAD_DIR || './uploads',
      ...config
    };
  }

  /**
   * Validate uploaded file
   */
  validateFile(file: File): { valid: boolean; error?: string } {
    // Check file size
    if (file.size > this.config.maxSize) {
      return {
        valid: false,
        error: `File size too large. Maximum ${this.config.maxSize / 1024 / 1024}MB allowed.`
      };
    }

    // Check file type
    if (!this.config.allowedTypes.includes(file.type)) {
      return {
        valid: false,
        error: `Invalid file type. Allowed types: ${this.config.allowedTypes.join(', ')}`
      };
    }

    return { valid: true };
  }

  /**
   * Sanitize filename to prevent path traversal attacks
   */
  sanitizeFilename(filename: string): string {
    return filename
      .replace(/[^a-zA-Z0-9.-]/g, '_')
      .replace(/_{2,}/g, '_')
      .toLowerCase();
  }

  /**
   * Generate unique filename with timestamp
   */
  generateFilename(originalName: string): string {
    const timestamp = Date.now();
    const sanitized = this.sanitizeFilename(originalName);
    const ext = path.extname(sanitized);
    const name = path.basename(sanitized, ext);
    return `${timestamp}-${name}${ext}`;
  }

  /**
   * Ensure upload directory exists
   */
  async ensureUploadDir(subDir?: string): Promise<string> {
    const uploadPath = subDir 
      ? path.join(this.config.uploadDir, subDir)
      : this.config.uploadDir;

    try {
      await access(uploadPath, constants.F_OK);
    } catch {
      await mkdir(uploadPath, { recursive: true });
    }

    return uploadPath;
  }

  /**
   * Upload file to local storage
   */
  async uploadFile(file: File, subDir: string = 'resumes'): Promise<UploadedFile> {
    // Validate file
    const validation = this.validateFile(file);
    if (!validation.valid) {
      throw new Error(validation.error);
    }

    // Ensure upload directory exists
    const uploadDir = await this.ensureUploadDir(subDir);

    // Generate unique filename
    const filename = this.generateFilename(file.name);
    const filePath = path.join(uploadDir, filename);

    // Convert file to buffer and save
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    await writeFile(filePath, buffer);

    // Return file information
    return {
      filename,
      originalName: file.name,
      path: filePath,
      size: file.size,
      mimetype: file.type,
      url: `/uploads/${subDir}/${filename}`
    };
  }

  /**
   * Extract file from FormData
   */
  async extractFileFromFormData(formData: FormData, fieldName: string): Promise<File | null> {
    const file = formData.get(fieldName);
    
    if (!file || !(file instanceof File)) {
      return null;
    }

    return file;
  }

  /**
   * Handle multiple file uploads
   */
  async uploadMultipleFiles(files: File[], subDir: string = 'resumes'): Promise<UploadedFile[]> {
    const uploadPromises = files.map(file => this.uploadFile(file, subDir));
    return Promise.all(uploadPromises);
  }

  /**
   * Get file extension from mimetype
   */
  getExtensionFromMimetype(mimetype: string): string {
    const mimeToExt: Record<string, string> = {
      'application/pdf': '.pdf',
      'application/msword': '.doc',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
      'text/plain': '.txt',
      'image/jpeg': '.jpg',
      'image/png': '.png'
    };

    return mimeToExt[mimetype] || '';
  }

  /**
   * Delete file from storage
   */
  async deleteFile(filePath: string): Promise<boolean> {
    try {
      const { unlink } = await import('fs/promises');
      await unlink(filePath);
      return true;
    } catch (error) {
      console.error('Error deleting file:', error);
      return false;
    }
  }
}

// Export singleton instance
export const fileStorage = new FileStorageService();

// Export types
export type { FileUploadConfig, UploadedFile };
