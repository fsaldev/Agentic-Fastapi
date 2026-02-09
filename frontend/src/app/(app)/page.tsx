"use client";

import Link from "next/link";
import { Car, Users, Calendar, Plus, AlertCircle } from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { PageHeader } from "@/components/shared/page-header";
import { StatusBadge } from "@/components/shared/status-badge";
import { useCars } from "@/lib/hooks/use-cars";
import { useBookings } from "@/lib/hooks/use-bookings";
import { useCustomers } from "@/lib/hooks/use-customers";
import { format } from "date-fns";

function StatCardSkeleton() {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <Skeleton className="h-4 w-24" />
        <Skeleton className="h-4 w-4" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-8 w-16" />
        <Skeleton className="mt-1 h-3 w-20" />
      </CardContent>
    </Card>
  );
}

function TableSkeleton() {
  return (
    <div className="space-y-3">
      {Array.from({ length: 5 }).map((_, i) => (
        <Skeleton key={i} className="h-12 w-full" />
      ))}
    </div>
  );
}

export default function DashboardPage() {
  const { cars, isLoading: carsLoading, isError: carsError } = useCars();
  const {
    bookings,
    isLoading: bookingsLoading,
    isError: bookingsError,
  } = useBookings();
  const {
    customers,
    isLoading: customersLoading,
    isError: customersError,
  } = useCustomers();

  const isLoading = carsLoading || bookingsLoading || customersLoading;
  const isError = carsError || bookingsError || customersError;

  const totalCars = cars?.length ?? 0;
  const availableCars = cars?.filter((c) => c.status === "available").length ?? 0;
  const activeRentals =
    bookings?.filter((b) => b.status === "active").length ?? 0;
  const totalCustomers = customers?.length ?? 0;

  const carsByStatus = {
    available: cars?.filter((c) => c.status === "available").length ?? 0,
    rented: cars?.filter((c) => c.status === "rented").length ?? 0,
    maintenance: cars?.filter((c) => c.status === "maintenance").length ?? 0,
  };

  const recentBookings = bookings
    ? [...bookings]
        .sort(
          (a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        )
        .slice(0, 5)
    : [];

  if (isError) {
    return (
      <div>
        <PageHeader
          title="Dashboard"
          description="Overview of your car rental business"
        />
        <div className="mt-6 flex flex-col items-center justify-center rounded-lg border border-destructive/50 bg-destructive/10 p-8">
          <AlertCircle className="h-10 w-10 text-destructive" />
          <h3 className="mt-4 text-lg font-semibold">Failed to load dashboard data</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Please check your connection and try again.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <PageHeader
        title="Dashboard"
        description="Overview of your car rental business"
      />

      {/* Stat Cards */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {isLoading ? (
          Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />)
        ) : (
          <>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Cars
                </CardTitle>
                <Car className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalCars}</div>
                <CardDescription>Fleet size</CardDescription>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Available Cars
                </CardTitle>
                <Car className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{availableCars}</div>
                <CardDescription>Ready to rent</CardDescription>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Active Rentals
                </CardTitle>
                <Calendar className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{activeRentals}</div>
                <CardDescription>Currently rented</CardDescription>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Customers
                </CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalCustomers}</div>
                <CardDescription>Registered customers</CardDescription>
              </CardContent>
            </Card>
          </>
        )}
      </div>

      {/* Cars by Status & Quick Actions */}
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Cars by Status</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-3">
                {Array.from({ length: 3 }).map((_, i) => (
                  <Skeleton key={i} className="h-6 w-full" />
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-green-500" />
                    <span className="text-sm">Available</span>
                  </div>
                  <span className="text-sm font-medium">
                    {carsByStatus.available}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-blue-500" />
                    <span className="text-sm">Rented</span>
                  </div>
                  <span className="text-sm font-medium">
                    {carsByStatus.rented}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-yellow-500" />
                    <span className="text-sm">Maintenance</span>
                  </div>
                  <span className="text-sm font-medium">
                    {carsByStatus.maintenance}
                  </span>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <Button asChild>
              <Link href="/bookings">
                <Plus className="h-4 w-4" />
                New Booking
              </Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/cars">
                <Plus className="h-4 w-4" />
                Add Car
              </Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/customers">
                <Plus className="h-4 w-4" />
                Add Customer
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Recent Bookings */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Recent Bookings</CardTitle>
          <CardDescription>Last 5 bookings</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <TableSkeleton />
          ) : recentBookings.length === 0 ? (
            <p className="text-sm text-muted-foreground">No bookings yet.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Car</TableHead>
                  <TableHead>Customer</TableHead>
                  <TableHead>Dates</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentBookings.map((booking) => {
                  const car = cars?.find((c) => c.id === booking.car_id);
                  const customer = customers?.find(
                    (c) => c.id === booking.customer_id
                  );
                  return (
                    <TableRow key={booking.id}>
                      <TableCell>
                        {car
                          ? `${car.make} ${car.model}`
                          : booking.car_id.slice(0, 8)}
                      </TableCell>
                      <TableCell>
                        {customer
                          ? `${customer.first_name} ${customer.last_name}`
                          : booking.customer_id.slice(0, 8)}
                      </TableCell>
                      <TableCell>
                        {format(new Date(booking.start_date), "MMM d")} -{" "}
                        {format(new Date(booking.end_date), "MMM d")}
                      </TableCell>
                      <TableCell>
                        <StatusBadge status={booking.status} />
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
