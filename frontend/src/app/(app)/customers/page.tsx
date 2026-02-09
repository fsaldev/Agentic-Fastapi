import { PageHeader } from "@/components/shared/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { Users } from "lucide-react";

export default function CustomersPage() {
  return (
    <div>
      <PageHeader
        title="Customers"
        description="Manage customer records"
      />
      <div className="mt-6">
        <EmptyState
          icon={Users}
          title="No customers yet"
          description="Add your first customer to get started."
          actionLabel="Add Customer"
        />
      </div>
    </div>
  );
}
