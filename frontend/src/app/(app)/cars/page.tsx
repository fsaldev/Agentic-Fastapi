import { PageHeader } from "@/components/shared/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { Car } from "lucide-react";

export default function CarsPage() {
  return (
    <div>
      <PageHeader
        title="Cars"
        description="Manage your vehicle fleet"
      />
      <div className="mt-6">
        <EmptyState
          icon={Car}
          title="No cars yet"
          description="Add your first vehicle to the fleet to get started."
          actionLabel="Add Car"
        />
      </div>
    </div>
  );
}
