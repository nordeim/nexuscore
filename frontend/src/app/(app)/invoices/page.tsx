/**
 * Invoices Page
 * Shows invoices with GST breakdown
 */
import { Button, Card, CardBody, CardHeader } from '@/components/ui';

const invoices = [
    { id: 'INV-2024-001', organization: 'Acme Pte Ltd', subtotal: 10000, gst: 900, total: 10900, status: 'paid', date: '2024-01-15' },
    { id: 'INV-2024-002', organization: 'Corp Pte Ltd', subtotal: 5000, gst: 450, total: 5450, status: 'open', date: '2024-01-18' },
    { id: 'INV-2024-003', organization: 'Tech Pte Ltd', subtotal: 2500, gst: 225, total: 2725, status: 'draft', date: '2024-01-20' },
];

const statusColors: Record<string, string> = {
    draft: 'bg-gray-100 text-gray-700',
    open: 'bg-blue-100 text-blue-700',
    paid: 'bg-green-100 text-green-700',
    void: 'bg-red-100 text-red-700',
};

export default function InvoicesPage() {
    return (
        <div>
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl font-bold text-dark-900 dark:text-white">
                    Invoices
                </h1>
                <Button>Create Invoice</Button>
            </div>

            {/* GST Info */}
            <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <p className="text-sm text-blue-700 dark:text-blue-300">
                    <strong>GST Note:</strong> All invoices include 9% GST as per IRAS requirements.
                    Transaction codes: SR (Standard-Rated), ZR (Zero-Rated), OS (Out-of-Scope), TX (Exempted).
                </p>
            </div>

            <Card>
                <CardHeader>
                    <div className="flex items-center gap-4">
                        <input
                            type="text"
                            placeholder="Search invoices..."
                            className="flex-1 px-4 py-2 border border-dark-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-800 text-dark-900 dark:text-white"
                        />
                        <select className="px-4 py-2 border border-dark-300 dark:border-dark-600 rounded-lg bg-white dark:bg-dark-800 text-dark-900 dark:text-white">
                            <option value="">All Status</option>
                            <option value="draft">Draft</option>
                            <option value="open">Open</option>
                            <option value="paid">Paid</option>
                        </select>
                    </div>
                </CardHeader>
                <CardBody className="p-0">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-dark-200 dark:border-dark-700">
                                <th className="px-6 py-3 text-left text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Invoice
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Organization
                                </th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Subtotal
                                </th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    GST (9%)
                                </th>
                                <th className="px-6 py-3 text-right text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Total
                                </th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-dark-500 uppercase tracking-wider">
                                    Status
                                </th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-dark-200 dark:divide-dark-700">
                            {invoices.map((invoice) => (
                                <tr key={invoice.id} className="hover:bg-dark-50 dark:hover:bg-dark-800">
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <p className="text-sm font-medium text-dark-900 dark:text-white">
                                                {invoice.id}
                                            </p>
                                            <p className="text-xs text-dark-500">{invoice.date}</p>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-dark-600 dark:text-dark-300">
                                        {invoice.organization}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-dark-900 dark:text-white">
                                        ${(invoice.subtotal / 100).toFixed(2)}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-dark-600 dark:text-dark-300">
                                        ${(invoice.gst / 100).toFixed(2)}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-medium text-dark-900 dark:text-white">
                                        ${(invoice.total / 100).toFixed(2)}
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2 py-1 text-xs font-medium rounded capitalize ${statusColors[invoice.status]}`}>
                                            {invoice.status}
                                        </span>
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
