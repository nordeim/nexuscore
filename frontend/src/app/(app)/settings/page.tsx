/**
 * Settings Page
 */
import { Button, Input, Card, CardBody, CardHeader } from '@/components/ui';

export default function SettingsPage() {
    return (
        <div>
            <h1 className="text-2xl font-bold text-dark-900 dark:text-white mb-6">
                Settings
            </h1>

            <div className="space-y-6">
                {/* Profile */}
                <Card>
                    <CardHeader>
                        <h2 className="text-lg font-semibold text-dark-900 dark:text-white">
                            Profile
                        </h2>
                    </CardHeader>
                    <CardBody>
                        <div className="grid md:grid-cols-2 gap-6">
                            <Input label="Full Name" defaultValue="John Doe" />
                            <Input label="Email" type="email" defaultValue="john@company.com" disabled />
                            <Input label="Company" defaultValue="Company Pte Ltd" />
                            <Input label="Timezone" defaultValue="Asia/Singapore" disabled />
                        </div>
                        <div className="mt-6">
                            <Button>Save Changes</Button>
                        </div>
                    </CardBody>
                </Card>

                {/* Organization */}
                <Card>
                    <CardHeader>
                        <h2 className="text-lg font-semibold text-dark-900 dark:text-white">
                            Organization
                        </h2>
                    </CardHeader>
                    <CardBody>
                        <div className="grid md:grid-cols-2 gap-6">
                            <Input label="Organization Name" defaultValue="Company Pte Ltd" />
                            <Input label="UEN" defaultValue="202312345A" helperText="Unique Entity Number (Singapore)" />
                            <Input label="GST Registration Number" defaultValue="M12345678A" helperText="Leave blank if not GST registered" />
                            <Input label="Billing Email" type="email" defaultValue="billing@company.com" />
                        </div>
                        <div className="mt-6">
                            <Button>Update Organization</Button>
                        </div>
                    </CardBody>
                </Card>

                {/* PDPA */}
                <Card>
                    <CardHeader>
                        <h2 className="text-lg font-semibold text-dark-900 dark:text-white">
                            PDPA & Privacy
                        </h2>
                    </CardHeader>
                    <CardBody>
                        <p className="text-dark-500 mb-4">
                            Under the Personal Data Protection Act (PDPA), you have the right to access, correct, or delete your personal data.
                        </p>
                        <div className="flex gap-4">
                            <Button variant="outline">Export My Data</Button>
                            <Button variant="danger">Request Data Deletion</Button>
                        </div>
                    </CardBody>
                </Card>
            </div>
        </div>
    );
}
