/**
 * Leads Page
 */
import { Button, Card, CardBody, CardHeader } from '@/components/ui';

const leads = [
    { id: 1, name: 'John Doe', email: 'john@company.com', company: 'Acme Pte Ltd', status: 'new', source: 'website' },
    { id: 2, name: 'Jane Smith', email: 'jane@corp.com', company: 'Corp Pte Ltd', status: 'contacted', source: 'demo_request' },
    { id: 3, name: 'Bob Wilson', email: 'bob@tech.com', company: 'Tech Pte Ltd', status: 'qualified', source: 'referral' },
];

const statusColors: Record<string, string> = {
    new: 'bg-blue-100 text-blue-700',
    contacted: 'bg-yellow-100 text-yellow-700',
    qualified: 'bg-purple-100 text-purple-700',
    converted: 'bg-green-100 text-green-700',
    disqualified: 'bg-red-100 text-red-700',
};

export default function LeadsPage() {
    return (
        <div>
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl font-bold text-dark-900 dark:text-white">
                    Leads
                </h1>
                <Button>Add Lead</Button>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center gap-4">
                        <input
                            type="text"
                            placeholder="Search leads..."
                            className="flex-1 px-4 py-2 border border-dark-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-800 text-dark-900 dark:text-white"
                        />
                        <select className="px-4 py-2 border border-dark-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-800 text-dark-900 dark:text-white">
                            <option value="">All Status</option>
                            <option value="new">New</option>
                            <option value="contacted">Contacted</option>
                            <option value="qualified">Qualified</option>
                        </select>
                    </div>
                </CardHeader>
                <CardBody className="p-0">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-dark-200 dark:border-dark-700">
                                <th className="px-6 py-3 text-left text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Name
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Company
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Source
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Status
                                </th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-dark-200 dark:divide-dark-700">
                            {leads.map((lead) => (
                                <tr key={lead.id} className="hover:bg-dark-50 dark:hover:bg-dark-800">
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <p className="text-sm font-medium text-dark-900 dark:text-white">
                                                {lead.name}
                                            </p>
                                            <p className="text-sm text-dark-500">{lead.email}</p>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-dark-600 dark:text-dark-300">
                                        {lead.company}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-dark-600 dark:text-dark-300 capitalize">
                                        {lead.source.replace('_', ' ')}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2 py-1 text-xs font-medium rounded capitalize ${statusColors[lead.status]}`}>
                                            {lead.status}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                                        <button className="text-singapore-red hover:underline">
                                            View
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </CardBody>
            </Card>
        </div>
    );
}
