/**
 * Homepage
 * Marketing landing page
 */
import { Hero } from '@/components/marketing';

export default function HomePage() {
  return (
    <main>
      <Hero />

      {/* Features Section */}
      <section className="py-24 bg-white dark:bg-dark-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-dark-900 dark:text-white">
              Built for Singapore
            </h2>
            <p className="mt-4 text-lg text-dark-500">
              Everything you need to run your business, compliant with local regulations.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* GST Compliance */}
            <div className="text-center p-6">
              <div className="w-16 h-16 mx-auto mb-4 bg-singapore-red/10 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-singapore-red" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-dark-900 dark:text-white mb-2">
                GST Compliant
              </h3>
              <p className="text-dark-500">
                Automatic 9% GST calculation with IRAS transaction codes.
              </p>
            </div>

            {/* PDPA Ready */}
            <div className="text-center p-6">
              <div className="w-16 h-16 mx-auto mb-4 bg-secondary-800/10 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-secondary-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-dark-900 dark:text-white mb-2">
                PDPA Ready
              </h3>
              <p className="text-dark-500">
                72-hour DSAR handling with manual approval for deletions.
              </p>
            </div>

            {/* Singapore Timezone */}
            <div className="text-center p-6">
              <div className="w-16 h-16 mx-auto mb-4 bg-green-500/10 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-dark-900 dark:text-white mb-2">
                SGT Timezone
              </h3>
              <p className="text-dark-500">
                Default Asia/Singapore timezone for all operations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-singapore-red to-secondary-800">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to get started?
          </h2>
          <p className="text-lg text-white/80 mb-8">
            Join hundreds of Singapore businesses already using NexusCore.
          </p>
          <a
            href="/signup"
            className="inline-block px-8 py-4 bg-white text-singapore-red font-semibold rounded-lg hover:bg-dark-100 transition-colors"
          >
            Start Your Free Trial
          </a>
        </div>
      </section>
    </main>
  );
}
