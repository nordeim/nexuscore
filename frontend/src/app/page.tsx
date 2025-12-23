/**
 * Homepage
 * Premium marketing landing page for NexusCore
 */
import Link from 'next/link';
import { Button } from '@/components/ui';

// Animated gradient text component
function GradientText({ children }: { children: React.ReactNode }) {
  return (
    <span className="bg-gradient-to-r from-singapore-red via-orange-500 to-singapore-red bg-[length:200%_auto] animate-gradient bg-clip-text text-transparent">
      {children}
    </span>
  );
}

// Stats card with glassmorphism
function StatCard({ value, label }: { value: string; label: string }) {
  return (
    <div className="relative group">
      <div className="absolute inset-0 bg-gradient-to-r from-singapore-red/20 to-secondary-500/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100" />
      <div className="relative bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-singapore-red/50 transition-all duration-300">
        <div className="text-4xl font-bold text-white mb-1">{value}</div>
        <div className="text-dark-400 text-sm">{label}</div>
      </div>
    </div>
  );
}

// Feature card with hover effects
function FeatureCard({
  icon,
  title,
  description,
  gradient
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  gradient: string;
}) {
  return (
    <div className="group relative">
      <div className={`absolute -inset-0.5 ${gradient} rounded-2xl blur opacity-25 group-hover:opacity-75 transition duration-500`} />
      <div className="relative bg-dark-900 border border-dark-700 rounded-2xl p-8 hover:border-dark-500 transition-all duration-300">
        <div className={`w-14 h-14 ${gradient} rounded-xl flex items-center justify-center mb-6 shadow-lg`}>
          {icon}
        </div>
        <h3 className="text-xl font-semibold text-white mb-3">{title}</h3>
        <p className="text-dark-400 leading-relaxed">{description}</p>
      </div>
    </div>
  );
}

// Testimonial card
function TestimonialCard({
  quote,
  author,
  role,
  company
}: {
  quote: string;
  author: string;
  role: string;
  company: string;
}) {
  return (
    <div className="bg-gradient-to-br from-dark-800 to-dark-900 border border-dark-700 rounded-2xl p-8">
      <div className="flex gap-1 mb-4">
        {[...Array(5)].map((_, i) => (
          <svg key={i} className="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        ))}
      </div>
      <blockquote className="text-dark-200 text-lg leading-relaxed mb-6">
        &ldquo;{quote}&rdquo;
      </blockquote>
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 bg-gradient-to-br from-singapore-red to-secondary-600 rounded-full flex items-center justify-center text-white font-bold">
          {author.charAt(0)}
        </div>
        <div>
          <div className="text-white font-medium">{author}</div>
          <div className="text-dark-400 text-sm">{role}, {company}</div>
        </div>
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <main className="bg-dark-950 overflow-hidden">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center">
        {/* Animated background */}
        <div className="absolute inset-0">
          <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-singapore-red/20 rounded-full blur-[120px] animate-pulse" />
          <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-secondary-600/20 rounded-full blur-[100px] animate-pulse" style={{ animationDelay: '1s' }} />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-purple-600/10 rounded-full blur-[150px]" />
        </div>

        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:100px_100px]" />

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32">
          <div className="text-center">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-full mb-8 backdrop-blur-sm">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-dark-300 text-sm">Trusted by 500+ Singapore businesses</span>
            </div>

            {/* Main heading */}
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
              Enterprise SaaS
              <br />
              Built for <GradientText>Singapore</GradientText>
            </h1>

            {/* Subheading */}
            <p className="text-xl text-dark-300 max-w-2xl mx-auto mb-10 leading-relaxed">
              The only platform with <span className="text-white font-medium">database-level GST compliance</span>,
              {' '}<span className="text-white font-medium">72-hour PDPA automation</span>, and {' '}
              <span className="text-white font-medium">UEN validation</span> built-in.
            </p>

            {/* CTA buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Link href="/signup">
                <Button size="lg" className="px-8 py-4 text-lg bg-gradient-to-r from-singapore-red to-orange-600 hover:from-singapore-red hover:to-orange-500 border-0 shadow-lg shadow-singapore-red/25">
                  Start Free Trial
                  <svg className="w-5 h-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Button>
              </Link>
              <Link href="#demo">
                <Button variant="outline" size="lg" className="px-8 py-4 text-lg border-dark-600 text-white hover:bg-white/5">
                  <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Watch Demo
                </Button>
              </Link>
            </div>

            {/* Trust signals */}
            <p className="text-dark-500 text-sm">
              ✓ No credit card required • ✓ 14-day free trial • ✓ Cancel anytime
            </p>
          </div>

          {/* Stats row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20">
            <StatCard value="9%" label="GST Auto-Calculated" />
            <StatCard value="72hr" label="PDPA SLA Guarantee" />
            <StatCard value="99.9%" label="Uptime SLA" />
            <StatCard value="$0" label="Setup Fees" />
          </div>
        </div>
      </section>

      {/* Platform Preview Section */}
      <section className="relative py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative">
            {/* Glow effect */}
            <div className="absolute -inset-4 bg-gradient-to-r from-singapore-red/20 via-purple-500/20 to-secondary-500/20 rounded-3xl blur-2xl" />

            {/* Dashboard mockup */}
            <div className="relative bg-dark-900 border border-dark-700 rounded-2xl overflow-hidden shadow-2xl">
              {/* Window controls */}
              <div className="flex items-center gap-2 px-4 py-3 bg-dark-800 border-b border-dark-700">
                <div className="w-3 h-3 rounded-full bg-red-500" />
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <div className="w-3 h-3 rounded-full bg-green-500" />
                <span className="ml-4 text-dark-400 text-sm">NexusCore Dashboard</span>
              </div>

              {/* Dashboard content preview */}
              <div className="p-6 bg-gradient-to-br from-dark-900 to-dark-950">
                <div className="grid grid-cols-4 gap-4 mb-6">
                  {['Total Leads', 'Active Subscriptions', 'Revenue (SGD)', 'Invoices'].map((label, i) => (
                    <div key={i} className="bg-dark-800/50 border border-dark-700 rounded-xl p-4">
                      <div className="text-dark-400 text-sm mb-1">{label}</div>
                      <div className="text-2xl font-bold text-white">
                        {i === 0 ? '1,234' : i === 1 ? '45' : i === 2 ? '$12,450' : '7'}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="h-48 bg-dark-800/30 border border-dark-700 rounded-xl flex items-center justify-center">
                  <span className="text-dark-500">📊 Real-time Analytics Dashboard</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-dark-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Built Different. Built for <span className="text-singapore-red">Singapore</span>.
            </h2>
            <p className="text-xl text-dark-400 max-w-2xl mx-auto">
              Not just another SaaS platform. Purpose-built compliance at the database level.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              gradient="bg-gradient-to-br from-singapore-red to-orange-600"
              icon={
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              }
              title="Database-Level GST"
              description="GST calculated using PostgreSQL GeneratedField. Zero floating-point errors, perfect IRAS compliance, immutable audit trail."
            />

            <FeatureCard
              gradient="bg-gradient-to-br from-secondary-600 to-blue-600"
              icon={
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              }
              title="PDPA Automation"
              description="72-hour DSAR SLA with automated tracking. Manual deletion approval required. Full compliance with Singapore's data protection laws."
            />

            <FeatureCard
              gradient="bg-gradient-to-br from-green-500 to-emerald-600"
              icon={
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              }
              title="UEN Validation"
              description="Built-in ACRA format validation. Supports all UEN formats including company, business, and other entity types."
            />
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-24 bg-gradient-to-b from-dark-950 to-dark-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Trusted by Singapore Businesses
            </h2>
            <p className="text-xl text-dark-400">
              See what our customers are saying
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <TestimonialCard
              quote="Finally, a platform that understands Singapore compliance. GST and PDPA handled automatically."
              author="Sarah Lim"
              role="CEO"
              company="TechStart Pte Ltd"
            />
            <TestimonialCard
              quote="The 72-hour DSAR automation saved us countless hours. Our compliance team loves it."
              author="Michael Tan"
              role="CTO"
              company="DataFlow Solutions"
            />
            <TestimonialCard
              quote="Database-level GST calculation means zero discrepancies. Our accountant is thrilled."
              author="Jennifer Wong"
              role="CFO"
              company="Growth Partners"
            />
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="py-24 bg-dark-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Built on Modern Tech
            </h2>
            <p className="text-xl text-dark-400">
              Enterprise-grade architecture from day one
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-8 items-center opacity-70">
            {['Django 6.0', 'Next.js 14', 'PostgreSQL 16', 'Redis 7.4', 'Celery', 'TypeScript'].map((tech) => (
              <div key={tech} className="px-6 py-3 bg-dark-800 border border-dark-700 rounded-full text-dark-300 font-mono text-sm">
                {tech}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-singapore-red to-secondary-800" />
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:50px_50px]" />

        <div className="relative max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl sm:text-5xl font-bold text-white mb-6">
            Ready to Go Compliant?
          </h2>
          <p className="text-xl text-white/80 mb-10 max-w-2xl mx-auto">
            Join 500+ Singapore businesses running on NexusCore.
            Start your free 14-day trial today.
          </p>
          <Link href="/signup">
            <button className="px-10 py-5 bg-white text-singapore-red font-bold text-lg rounded-xl hover:bg-dark-100 transition-all duration-300 shadow-2xl shadow-black/25 hover:shadow-black/40 hover:scale-105">
              Start Free Trial →
            </button>
          </Link>
        </div>
      </section>
    </main>
  );
}
