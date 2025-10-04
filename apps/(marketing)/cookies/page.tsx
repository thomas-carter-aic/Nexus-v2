import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Cookie Policy - Applied Innovations Corporation',
  description: 'Cookie policy for Applied Innovations Corporation. Learn how we use cookies and similar technologies on our website.',
};

export default function CookiePolicyPage() {
  return (
    <div className="bg-white">
      <div className="container py-16">
        <div className="mx-auto max-w-4xl">
          <h1 className="text-4xl font-bold text-secondary-900 mb-8">Cookie Policy</h1>
          
          <div className="prose prose-lg max-w-none">
            <p className="text-lg text-secondary-600 mb-8">
              <strong>Last updated:</strong> July 4, 2024
            </p>

            <div className="space-y-8">
              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">1. What Are Cookies</h2>
                <p className="text-secondary-700 mb-4">
                  Cookies are small text files that are placed on your computer or mobile device when you visit our website. 
                  They are widely used to make websites work more efficiently and provide information to website owners.
                </p>
                <p className="text-secondary-700">
                  Cookies allow us to recognize your device and store some information about your preferences or past actions 
                  to improve your experience on our website.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">2. How We Use Cookies</h2>
                <p className="text-secondary-700 mb-4">
                  We use cookies for several purposes:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-2">
                  <li><strong>Essential Cookies:</strong> Required for the website to function properly</li>
                  <li><strong>Performance Cookies:</strong> Help us understand how visitors interact with our website</li>
                  <li><strong>Functionality Cookies:</strong> Remember your preferences and settings</li>
                  <li><strong>Marketing Cookies:</strong> Used to deliver relevant advertisements and track campaign effectiveness</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">3. Types of Cookies We Use</h2>
                
                <h3 className="text-xl font-semibold text-secondary-900 mb-3">3.1 Essential Cookies</h3>
                <p className="text-secondary-700 mb-4">
                  These cookies are necessary for the website to function and cannot be switched off in our systems. 
                  They are usually only set in response to actions made by you which amount to a request for services.
                </p>
                <div className="bg-secondary-50 p-4 rounded-lg mb-4">
                  <p className="text-sm text-secondary-700">
                    <strong>Examples:</strong> Session management, security tokens, load balancing
                  </p>
                </div>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">3.2 Analytics Cookies</h3>
                <p className="text-secondary-700 mb-4">
                  These cookies allow us to count visits and traffic sources so we can measure and improve 
                  the performance of our site. They help us know which pages are most and least popular.
                </p>
                <div className="bg-secondary-50 p-4 rounded-lg mb-4">
                  <p className="text-sm text-secondary-700">
                    <strong>Examples:</strong> Google Analytics, page view tracking, user behavior analysis
                  </p>
                </div>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">3.3 Functional Cookies</h3>
                <p className="text-secondary-700 mb-4">
                  These cookies enable the website to provide enhanced functionality and personalization. 
                  They may be set by us or by third-party providers whose services we have added to our pages.
                </p>
                <div className="bg-secondary-50 p-4 rounded-lg mb-4">
                  <p className="text-sm text-secondary-700">
                    <strong>Examples:</strong> Language preferences, theme settings, form data
                  </p>
                </div>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">3.4 Marketing Cookies</h3>
                <p className="text-secondary-700 mb-4">
                  These cookies may be set through our site by our advertising partners. They may be used 
                  to build a profile of your interests and show you relevant adverts on other sites.
                </p>
                <div className="bg-secondary-50 p-4 rounded-lg">
                  <p className="text-sm text-secondary-700">
                    <strong>Examples:</strong> Ad targeting, conversion tracking, remarketing
                  </p>
                </div>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">4. Third-Party Cookies</h2>
                <p className="text-secondary-700 mb-4">
                  We may also use third-party services that set cookies on your device. These include:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-2">
                  <li><strong>Google Analytics:</strong> For website analytics and performance measurement</li>
                  <li><strong>Google Ads:</strong> For advertising and conversion tracking</li>
                  <li><strong>LinkedIn:</strong> For professional networking and B2B marketing</li>
                  <li><strong>HubSpot:</strong> For customer relationship management and marketing automation</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">5. Managing Your Cookie Preferences</h2>
                <p className="text-secondary-700 mb-4">
                  You have several options for managing cookies:
                </p>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">5.1 Browser Settings</h3>
                <p className="text-secondary-700 mb-4">
                  Most web browsers allow you to control cookies through their settings preferences. 
                  You can set your browser to:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 mb-4 space-y-1">
                  <li>Block all cookies</li>
                  <li>Block third-party cookies only</li>
                  <li>Delete cookies when you close your browser</li>
                  <li>Ask for your permission before accepting cookies</li>
                </ul>

                <h3 className="text-xl font-semibold text-secondary-900 mb-3">5.2 Cookie Consent Tool</h3>
                <p className="text-secondary-700 mb-4">
                  When you first visit our website, you'll see a cookie consent banner that allows you to:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>Accept all cookies</li>
                  <li>Reject non-essential cookies</li>
                  <li>Customize your cookie preferences</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">6. Cookie Retention</h2>
                <p className="text-secondary-700 mb-4">
                  Different cookies have different lifespans:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-2">
                  <li><strong>Session Cookies:</strong> Deleted when you close your browser</li>
                  <li><strong>Persistent Cookies:</strong> Remain on your device for a set period (typically 30 days to 2 years)</li>
                  <li><strong>Analytics Cookies:</strong> Usually expire after 2 years</li>
                  <li><strong>Marketing Cookies:</strong> Typically expire after 30-90 days</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">7. Impact of Disabling Cookies</h2>
                <p className="text-secondary-700 mb-4">
                  If you choose to disable cookies, some features of our website may not function properly:
                </p>
                <ul className="list-disc pl-6 text-secondary-700 space-y-1">
                  <li>You may need to re-enter information on each visit</li>
                  <li>Some personalized features may not work</li>
                  <li>We may not be able to remember your preferences</li>
                  <li>Website performance analytics will be limited</li>
                </ul>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">8. Updates to This Policy</h2>
                <p className="text-secondary-700">
                  We may update this Cookie Policy from time to time to reflect changes in our practices 
                  or for other operational, legal, or regulatory reasons. We will notify you of any 
                  material changes by posting the updated policy on our website.
                </p>
              </section>

              <section>
                <h2 className="text-2xl font-bold text-secondary-900 mb-4">9. Contact Us</h2>
                <p className="text-secondary-700 mb-4">
                  If you have any questions about our use of cookies, please contact us:
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
