// Example usage of NewsletterForm component

import NewsletterForm from './NewsletterForm'

// 1. Simple newsletter form for homepage
export function HomePageNewsletter() {
  return (
    <section className="bg-blue-50 py-16">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Stay Updated with AI Innovations
        </h2>
        <p className="text-lg text-gray-600 mb-8">
          Get the latest insights on AI technology, industry trends, and Applied Innovations updates.
        </p>
        <div className="max-w-md mx-auto">
          <NewsletterForm 
            source="homepage-hero"
            placeholder="Your email address"
            buttonText="Get Updates"
          />
        </div>
      </div>
    </section>
  )
}

// 2. Inline newsletter form for blog/content pages
export function InlineNewsletter() {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 my-8">
      <h3 className="text-xl font-semibold text-gray-900 mb-2">
        Don't miss our latest insights
      </h3>
      <p className="text-gray-600 mb-4">
        Subscribe to get AI industry updates delivered to your inbox.
      </p>
      <NewsletterForm 
        source="blog-inline"
        className="max-w-sm"
        buttonText="Subscribe"
        showConsent={false}
      />
    </div>
  )
}

// 3. Footer newsletter signup
export function FooterNewsletter() {
  return (
    <div className="bg-gray-900 text-white py-12">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid md:grid-cols-2 gap-8 items-center">
          <div>
            <h3 className="text-2xl font-bold mb-2">Stay in the Loop</h3>
            <p className="text-gray-300">
              Join thousands of professionals getting AI insights and updates.
            </p>
          </div>
          <div>
            <NewsletterForm 
              source="footer"
              placeholder="Enter your email"
              buttonText="Subscribe"
              className="max-w-md ml-auto"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

// 4. Modal/popup newsletter form
export function NewsletterModal({ isOpen, onClose }: { isOpen: boolean, onClose: () => void }) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold text-gray-900">
            Get AI Insights
          </h3>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>
        <p className="text-gray-600 mb-6">
          Subscribe to our newsletter for the latest AI innovations and industry insights.
        </p>
        <NewsletterForm 
          source="popup-modal"
          buttonText="Subscribe Now"
        />
      </div>
    </div>
  )
}
