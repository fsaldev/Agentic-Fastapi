import { PageHeader } from "@/components/shared/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { Calendar } from "lucide-react";

export default function BookingsPage() {
  return (
    <div>
      <PageHeader
        title="Bookings"
        description="Manage car reservations and rentals"
      />
      <div className="mt-6">
        <EmptyState
          icon={Calendar}
          title="No bookings yet"
          description="Create your first booking to get started."
          actionLabel="New Booking"
        />
      </div>
    </div>
  );
}
