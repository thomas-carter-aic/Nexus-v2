import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy - Applied Innovations Corporation',
  description: 'Privacy policy for Applied Innovations Corporation. Learn how we collect, use, and protect your personal information.',
};

export default function PrivacyPolicyPage() {
  return (
    <div className="bg-white">
      <div className="container py-16">
        <div className="mx-auto max-w-4xl">
          <h1 className="text-4xl font-bold text-secondary-900 mb-8">Privacy Policy</h1>
          
          <div className="prose prose-lg max-w-none">
            <p className="text-lg text-secondary-600 mb-8">
              <strong>Last updated:</strong> July 4, 2024
            </p>

            <div className="space-y-8">
              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">1. Introduction</h2>
                <p className="text-secondary-700 mb-4">
                  Applied Innovations Corporation ("we," "our," or "us") is committed to protecting your privacy. 
                  This Privacy Policy explains how we collect, use, disclose, and safeguard your information when 
                  you visit our website, use our services, or interact with us.
                </p>
                <p className="text-secondary-700">
                  Please read this Privacy Policy carefully. If you do not agree with the terms of this Privacy Policy, 
                  please do not access our website or use our services.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">2. Information We Collect</h2>
                
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">2.1 Personal Information</h3>
                <p className="text-secondary-700 mb-4">
                  We may collect personal information that you voluntarily provide to us, including:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 mb-4 space-y-1">
                  <li>Name and contact information (email address, phone number, mailing address)</li>
                  <li>Company information and job title</li>
                  <li>Account credentials and profile information</li>
                  <li>Payment and billing information</li>
                  <li>Communications and correspondence with us</li>
                </ul>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">2.2 Automatically Collected Information</h3>
                <p className="text-secondary-700 mb-4">
                  When you visit our website or use our services, we may automatically collect:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 mb-4 space-y-1">
                  <li>Device and browser information</li>
                  <li>IP address and location data</li>
                  <li>Usage data and analytics</li>
                  <li>Cookies and similar tracking technologies</li>
                </ul>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">2.3 Business Data</h3>
                <p className="text-secondary-700">
                  When you use our AI services, we may process business data that you provide, including 
                  documents, datasets, and other information necessary to deliver our services.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">3. How We Use Your Information</h2>
                <p className="text-secondary-700 mb-4">
                  We use the information we collect for the following purposes:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>Provide, maintain, and improve our services</li>
                  <li>Process transactions and manage accounts</li>
                  <li>Communicate with you about our services</li>
                  <li>Provide customer support and technical assistance</li>
                  <li>Send marketing communications (with your consent)</li>
                  <li>Comply with legal obligations and protect our rights</li>
                  <li>Analyze usage patterns and improve user experience</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">4. Information Sharing and Disclosure</h2>
                <p className="text-secondary-700 mb-4">
                  We do not sell, trade, or rent your personal information to third parties. We may share 
                  your information in the following circumstances:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li><strong>Service Providers:</strong> With trusted third-party service providers who assist us in operating our business</li>
                  <li><strong>Legal Requirements:</strong> When required by law or to protect our rights and safety</li>
                  <li><strong>Business Transfers:</strong> In connection with a merger, acquisition, or sale of assets</li>
                  <li><strong>Consent:</strong> With your explicit consent for specific purposes</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">5. Data Security</h2>
                <p className="text-secondary-700 mb-4">
                  We implement appropriate technical and organizational security measures to protect your 
                  information against unauthorized access, alteration, disclosure, or destruction. These measures include:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>Encryption of data in transit and at rest</li>
                  <li>Access controls and authentication mechanisms</li>
                  <li>Regular security assessments and monitoring</li>
                  <li>Employee training on data protection practices</li>
                  <li>Compliance with industry security standards</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">6. Data Retention</h2>
                <p className="text-secondary-700">
                  We retain your personal information only for as long as necessary to fulfill the purposes 
                  outlined in this Privacy Policy, comply with legal obligations, resolve disputes, and 
                  enforce our agreements. When we no longer need your information, we will securely delete 
                  or anonymize it.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">7. Your Rights and Choices</h2>
                <p className="text-secondary-700 mb-4">
                  Depending on your location, you may have the following rights regarding your personal information:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li><strong>Access:</strong> Request access to your personal information</li>
                  <li><strong>Correction:</strong> Request correction of inaccurate information</li>
                  <li><strong>Deletion:</strong> Request deletion of your personal information</li>
                  <li><strong>Portability:</strong> Request a copy of your information in a portable format</li>
                  <li><strong>Opt-out:</strong> Opt out of marketing communications</li>
                  <li><strong>Restriction:</strong> Request restriction of processing in certain circumstances</li>
                </ul>
                <p className="text-secondary-700 mt-4">
                  To exercise these rights, please contact us at privacy@appliedinnovations.ai.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">8. Cookies and Tracking Technologies</h2>
                <p className="text-secondary-700 mb-4">
                  We use cookies and similar tracking technologies to enhance your experience on our website. 
                  You can control cookie settings through your browser preferences. For more information, 
                  please see our Cookie Policy.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">9. International Data Transfers</h2>
                <p className="text-secondary-700">
                  Your information may be transferred to and processed in countries other than your country 
                  of residence. We ensure appropriate safeguards are in place to protect your information 
                  in accordance with applicable data protection laws.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">10. Children's Privacy</h2>
                <p className="text-secondary-700">
                  Our services are not intended for children under the age of 13. We do not knowingly 
                  collect personal information from children under 13. If we become aware that we have 
                  collected such information, we will take steps to delete it promptly.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">11. Changes to This Privacy Policy</h2>
                <p className="text-secondary-700">
                  We may update this Privacy Policy from time to time. We will notify you of any material 
                  changes by posting the updated policy on our website and updating the "Last updated" date. 
                  Your continued use of our services after such changes constitutes acceptance of the updated policy.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">12. Contact Us</h2>
                <p className="text-secondary-700 mb-4">
                  If you have any questions about this Privacy Policy or our privacy practices, please contact us:
                </p>
                <div className="bg-secondary-50 p-6 rounded-lg">
                  <p className="text-secondary-700 mb-2"><strong>Applied Innovations Corporation</strong></p>
                  <p className="text-secondary-700 mb-2">Email: privacy@appliedinnovations.ai</p>
                  <p className="text-secondary-700 mb-2">Phone: +1 (555) AI-TRANSFORM</p>
                  <p className="text-secondary-700">
                    Address: 123 Innovation Drive, Tech Valley, CA 94000
                  </p>
                </div>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
