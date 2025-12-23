/**
 * Dashboard Page
 */
import { Card, CardBody, CardHeader } from '@/components/ui';

const stats = [
    { name: 'Total Leads', value: '1,234', change: '+12%', changeType: 'positive' },
    { name: 'Active Subscriptions', value: '45', change: '+3', changeType: 'positive' },
    { name: 'Revenue (SGD)', value: '$12,450', change: '+8%', changeType: 'positive' },
    { name: 'Outstanding Invoices', value: '7', change: '-2', changeType: 'neutral' },
];

export default function DashboardPage() {
    return (
        <div>
            <h1 className="text-2xl font-bold text-dark-900 dark:text-white mb-6">
                Dashboard
            </h1>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {stats.map((stat) => (
                    <Card key={stat.name}>
                        <CardBody className="p-6">
                            <p className="text-sm text-dark-500 mb-1">{stat.name}</p>
                            <p className="text-2xl font-bold text-dark-900 dark:text-white">
                                {stat.value}
                            </p>
                            <p className={`text-sm mt-1 ${stat.changeType === 'positive' ? 'text-green-600' : 'text-dark-500'
                                }`}>
                                {stat.change} from last month
                            </p>
                        </CardBody>
                    </Card>
                ))}
            </div>

            {/* Recent Activity */}
            <div className="grid lg:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <h2 className="text-lg font-semibold text-dark-900 dark:text-white">
                            Recent Leads
                        </h2>
                    </CardHeader>
                    <CardBody>
                        <div className="space-y-4">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="flex items-center gap-4 py-2">
                                    <div className="w-10 h-10 bg-primary-100 dark:bg-primary-900/20 rounded-full flex items-center justify-center">
                                        <span className="text-sm font-medium text-primary-600">L{i}</span>
                                    </div>
                                    <div className="flex-1">
                                        <p className="text-sm font-medium text-dark-900 dark:text-white">
                                            Lead #{i}
                                        </p>
                                        <p className="text-xs text-dark-500">
                                            lead{i}@company.com
                                        </p>
                                    </div>
                                    <span className="text-xs text-dark-400">
                                        2h ago
                                    </span>
                                </div>
                            ))}
                        </div>
                    </CardBody>
                </Card>

                <Card>
                    <CardHeader>
                        <h2 className="text-lg font-semibold text-dark-900 dark:text-white">
                            Recent Invoices
                        </h2>
                    </CardHeader>
                    <CardBody>
                        <div className="space-y-4">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="flex items-center gap-4 py-2">
                                    <div className="w-10 h-10 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
                                        <span className="text-sm font-medium text-green-600">$</span>
                                    </div>
                                    <div className="flex-1">
                                        <p className="text-sm font-medium text-dark-900 dark:text-white">
                                            INV-2024-00{i}
                                        </p>
                                        <p className="text-xs text-dark-500">
                                            ${(i * 100).toFixed(2)} + GST
                                        </p>
                                    </div>
                                    <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded">
                                        Paid
                                    </span>
                                </div>
                            ))}
                        </div>
                    </CardBody>
                </Card>
            </div>
        </div>
    );
}
