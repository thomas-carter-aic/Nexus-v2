import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Terms of Service - Applied Innovations Corporation',
  description: 'Terms of Service for Applied Innovations Corporation. Review the terms and conditions for using our AI services and platform.',
};

export default function TermsOfServicePage() {
  return (
    <div className="bg-white">
      <div className="container py-16">
        <div className="mx-auto max-w-4xl">
          <h1 className="text-4xl font-bold text-secondary-900 mb-8">Terms of Service</h1>
          
          <div className="prose prose-lg max-w-none">
            <p className="text-lg text-secondary-600 mb-8">
              <strong>Last updated:</strong> July 4, 2024
            </p>

            <div className="space-y-8">
              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">1. Acceptance of Terms</h2>
                <p className="text-secondary-700 mb-4">
                  These Terms of Service ("Terms") constitute a legally binding agreement between you and 
                  Applied Innovations Corporation ("Company," "we," "our," or "us") regarding your use of 
                  our website, services, and platform (collectively, the "Services").
                </p>
                <p className="text-secondary-700">
                  By accessing or using our Services, you agree to be bound by these Terms. If you do not 
                  agree to these Terms, you may not access or use our Services.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">2. Description of Services</h2>
                <p className="text-secondary-700 mb-4">
                  Applied Innovations Corporation provides AI consulting, transformation services, and our 
                  proprietary Nexus platform. Our Services include:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>AI strategy and assessment consulting</li>
                  <li>AI implementation and integration services</li>
                  <li>AI governance and compliance frameworks</li>
                  <li>Team training and enablement programs</li>
                  <li>Access to the Nexus AI platform</li>
                  <li>Ongoing support and optimization services</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">3. User Accounts and Registration</h2>
                <p className="text-secondary-700 mb-4">
                  To access certain features of our Services, you may be required to create an account. 
                  You agree to:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>Provide accurate, current, and complete information during registration</li>
                  <li>Maintain and update your account information</li>
                  <li>Keep your account credentials secure and confidential</li>
                  <li>Notify us immediately of any unauthorized use of your account</li>
                  <li>Accept responsibility for all activities under your account</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">4. Acceptable Use Policy</h2>
                <p className="text-secondary-700 mb-4">
                  You agree to use our Services only for lawful purposes and in accordance with these Terms. 
                  You agree not to:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>Violate any applicable laws or regulations</li>
                  <li>Infringe upon the rights of others</li>
                  <li>Upload or transmit malicious code or harmful content</li>
                  <li>Attempt to gain unauthorized access to our systems</li>
                  <li>Interfere with or disrupt our Services</li>
                  <li>Use our Services for competitive intelligence or benchmarking</li>
                  <li>Reverse engineer or attempt to extract source code</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">5. Intellectual Property Rights</h2>
                
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">5.1 Our Intellectual Property</h3>
                <p className="text-secondary-700 mb-4">
                  The Services, including the Nexus platform, and all related technology, software, and 
                  content are owned by us or our licensors and are protected by intellectual property laws. 
                  We grant you a limited, non-exclusive, non-transferable license to use our Services 
                  subject to these Terms.
                </p>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">5.2 Your Content</h3>
                <p className="text-secondary-700 mb-4">
                  You retain ownership of any data, content, or materials you provide to us ("Your Content"). 
                  By using our Services, you grant us a limited license to use Your Content solely to 
                  provide the Services to you.
                </p>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">5.3 Feedback</h3>
                <p className="text-secondary-700">
                  Any feedback, suggestions, or ideas you provide to us may be used by us without 
                  restriction or compensation to you.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">6. Payment Terms</h2>
                <p className="text-secondary-700 mb-4">
                  If you purchase our Services, you agree to pay all applicable fees as described in 
                  your service agreement or as posted on our website. Payment terms include:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>Fees are due and payable in advance unless otherwise agreed</li>
                  <li>All fees are non-refundable unless otherwise specified</li>
                  <li>You are responsible for all taxes and third-party fees</li>
                  <li>We may suspend Services for non-payment</li>
                  <li>Price changes will be communicated with 30 days' notice</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">7. Data Protection and Privacy</h2>
                <p className="text-secondary-700 mb-4">
                  We are committed to protecting your privacy and data. Our collection, use, and protection 
                  of your information is governed by our Privacy Policy, which is incorporated into these 
                  Terms by reference.
                </p>
                <p className="text-secondary-700">
                  For business data processed through our Services, we act as a data processor and will 
                  handle such data in accordance with applicable data protection laws and our Data 
                  Processing Agreement.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">8. Service Level Agreement</h2>
                <p className="text-secondary-700 mb-4">
                  We strive to provide reliable and high-quality Services. Our service level commitments 
                  include:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>99.9% uptime for the Nexus platform (excluding scheduled maintenance)</li>
                  <li>24/7 technical support for enterprise customers</li>
                  <li>Response times as specified in your service agreement</li>
                  <li>Regular security updates and monitoring</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">9. Limitation of Liability</h2>
                <p className="text-secondary-700 mb-4">
                  TO THE MAXIMUM EXTENT PERMITTED BY LAW, WE SHALL NOT BE LIABLE FOR ANY INDIRECT, 
                  INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED 
                  TO LOSS OF PROFITS, DATA, OR USE, ARISING OUT OF OR RELATING TO THESE TERMS OR 
                  THE SERVICES.
                </p>
                <p className="text-secondary-700">
                  OUR TOTAL LIABILITY TO YOU FOR ALL CLAIMS ARISING OUT OF OR RELATING TO THESE TERMS 
                  OR THE SERVICES SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO US IN THE TWELVE MONTHS 
                  PRECEDING THE CLAIM.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">10. Indemnification</h2>
                <p className="text-secondary-700">
                  You agree to indemnify, defend, and hold harmless Applied Innovations Corporation and 
                  its officers, directors, employees, and agents from any claims, damages, losses, or 
                  expenses arising out of your use of the Services, violation of these Terms, or 
                  infringement of any third-party rights.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">11. Termination</h2>
                <p className="text-secondary-700 mb-4">
                  Either party may terminate these Terms at any time with or without cause. Upon termination:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>Your access to the Services will be discontinued</li>
                  <li>You remain liable for all fees incurred prior to termination</li>
                  <li>We will return or delete Your Content as requested</li>
                  <li>Provisions that should survive termination will remain in effect</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">12. Dispute Resolution</h2>
                <p className="text-secondary-700 mb-4">
                  Any disputes arising out of or relating to these Terms shall be resolved through 
                  binding arbitration in accordance with the rules of the American Arbitration Association. 
                  The arbitration shall be conducted in San Francisco, California.
                </p>
                <p className="text-secondary-700">
                  You waive any right to participate in class action lawsuits or class-wide arbitrations.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">13. Governing Law</h2>
                <p className="text-secondary-700">
                  These Terms shall be governed by and construed in accordance with the laws of the 
                  State of California, without regard to its conflict of law principles.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">14. Changes to Terms</h2>
                <p className="text-secondary-700">
                  We reserve the right to modify these Terms at any time. We will provide notice of 
                  material changes by posting the updated Terms on our website and updating the 
                  "Last updated" date. Your continued use of the Services after such changes 
                  constitutes acceptance of the updated Terms.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">15. Miscellaneous</h2>
                <p className="text-secondary-700 mb-4">
                  These Terms constitute the entire agreement between you and us regarding the Services. 
                  If any provision is found to be unenforceable, the remaining provisions will remain 
                  in full force and effect.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">16. Contact Information</h2>
                <p className="text-secondary-700 mb-4">
                  If you have any questions about these Terms, please contact us:
                </p>
                <div className="bg-secondary-50 p-6 rounded-lg">
                  <p className="text-secondary-700 mb-2"><strong>Applied Innovations Corporation</strong></p>
                  <p className="text-secondary-700 mb-2">Email: legal@appliedinnovations.ai</p>
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
