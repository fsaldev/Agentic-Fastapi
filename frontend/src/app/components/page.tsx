"use client";

import * as React from "react";
import { toast } from "sonner";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

import { StatusBadge, type StatusType } from "@/components/shared/status-badge";
import { LoadingSpinner } from "@/components/shared/loading-spinner";
import { EmptyState } from "@/components/shared/empty-state";
import { PageHeader } from "@/components/shared/page-header";
import { DataTable, type ColumnDef, ArrowUpDown } from "@/components/shared/data-table";

import {
  AlertCircle,
  CheckCircle,
  ChevronDown,
  Info,
  MoreHorizontal,
  Search,
  Trash2,
} from "lucide-react";

// --- Sample data for DataTable ---
type Car = {
  id: number;
  make: string;
  model: string;
  year: number;
  dailyRate: number;
  status: StatusType;
};

const sampleCars: Car[] = [
  { id: 1, make: "Toyota", model: "Camry", year: 2024, dailyRate: 45, status: "available" },
  { id: 2, make: "Honda", model: "Civic", year: 2023, dailyRate: 40, status: "rented" },
  { id: 3, make: "BMW", model: "3 Series", year: 2024, dailyRate: 85, status: "maintenance" },
  { id: 4, make: "Tesla", model: "Model 3", year: 2025, dailyRate: 95, status: "reserved" },
  { id: 5, make: "Ford", model: "Mustang", year: 2023, dailyRate: 75, status: "available" },
  { id: 6, make: "Mercedes", model: "C-Class", year: 2024, dailyRate: 90, status: "rented" },
  { id: 7, make: "Audi", model: "A4", year: 2023, dailyRate: 80, status: "available" },
  { id: 8, make: "Chevrolet", model: "Malibu", year: 2022, dailyRate: 35, status: "completed" },
  { id: 9, make: "Nissan", model: "Altima", year: 2024, dailyRate: 42, status: "cancelled" },
  { id: 10, make: "Hyundai", model: "Sonata", year: 2023, dailyRate: 38, status: "active" },
];

const carColumns: ColumnDef<Car, unknown>[] = [
  {
    accessorKey: "make",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        Make
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "model",
    header: "Model",
  },
  {
    accessorKey: "year",
    header: ({ column }) => (
      <Button
        variant="ghost"
        onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      >
        Year
        <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "dailyRate",
    header: "Daily Rate",
    cell: ({ row }) => `$${row.getValue<number>("dailyRate")}/day`,
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => <StatusBadge status={row.getValue<StatusType>("status")} />,
  },
  {
    id: "actions",
    cell: ({ row }) => (
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" size="icon">
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuLabel>Actions</DropdownMenuLabel>
          <DropdownMenuItem onClick={() => toast.info(`Viewing ${row.original.make} ${row.original.model}`)}>
            View details
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => toast.info(`Editing ${row.original.make} ${row.original.model}`)}>
            Edit
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem className="text-destructive" onClick={() => toast.error(`Deleted ${row.original.make} ${row.original.model}`)}>
            Delete
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    ),
  },
];

// --- Form schema ---
const formSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  notes: z.string().optional(),
});

// --- Section wrapper ---
function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
      <Separator />
      {children}
    </div>
  );
}

export default function ComponentShowcase() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { name: "", email: "", notes: "" },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    toast.success(`Form submitted: ${values.name} (${values.email})`);
  }

  const statuses: StatusType[] = [
    "available", "rented", "maintenance", "reserved", "active", "completed", "cancelled",
  ];

  return (
    <div className="min-h-screen bg-background">
      <div className="mx-auto max-w-5xl space-y-12 p-8">
        {/* Page Header */}
        <PageHeader
          title="Component Showcase"
          description="All UI components from the Core UI Components Library (ACA-776)"
          breadcrumbs={[
            { label: "Home", href: "/" },
            { label: "Components" },
          ]}
          actions={
            <Button onClick={() => toast.success("Action button clicked!")}>
              Action Button
            </Button>
          }
        />

        {/* Buttons */}
        <Section title="Buttons">
          <div className="flex flex-wrap gap-3">
            <Button variant="default">Default</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="link">Link</Button>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button size="sm">Small</Button>
            <Button size="default">Default</Button>
            <Button size="lg">Large</Button>
            <Button disabled>Disabled</Button>
          </div>
        </Section>

        {/* Badges */}
        <Section title="Badges">
          <div className="space-y-4">
            <div>
              <h3 className="mb-2 text-sm font-medium text-muted-foreground">Base Badge</h3>
              <div className="flex flex-wrap gap-2">
                <Badge variant="default">Default</Badge>
                <Badge variant="secondary">Secondary</Badge>
                <Badge variant="destructive">Destructive</Badge>
                <Badge variant="outline">Outline</Badge>
              </div>
            </div>
            <div>
              <h3 className="mb-2 text-sm font-medium text-muted-foreground">Status Badge</h3>
              <div className="flex flex-wrap gap-2">
                {statuses.map((status) => (
                  <StatusBadge key={status} status={status} />
                ))}
              </div>
            </div>
          </div>
        </Section>

        {/* Cards */}
        <Section title="Cards">
          <div className="grid gap-4 sm:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>Total Cars</CardTitle>
                <CardDescription>Fleet overview</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold">42</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Active Rentals</CardTitle>
                <CardDescription>Currently rented</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold">18</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Revenue</CardTitle>
                <CardDescription>This month</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-3xl font-bold">$12,450</p>
              </CardContent>
              <CardFooter>
                <p className="text-sm text-muted-foreground">+12% from last month</p>
              </CardFooter>
            </Card>
          </div>
        </Section>

        {/* Form Components */}
        <Section title="Form Components">
          <Card>
            <CardHeader>
              <CardTitle>Sample Form</CardTitle>
              <CardDescription>React Hook Form + Zod validation</CardDescription>
            </CardHeader>
            <CardContent>
              <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                  <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Name</FormLabel>
                        <FormControl>
                          <Input placeholder="John Doe" {...field} />
                        </FormControl>
                        <FormDescription>Your full name</FormDescription>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Email</FormLabel>
                        <FormControl>
                          <Input type="email" placeholder="john@example.com" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <div className="space-y-2">
                    <Label>Car Type</Label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Select a car type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="sedan">Sedan</SelectItem>
                        <SelectItem value="suv">SUV</SelectItem>
                        <SelectItem value="sports">Sports</SelectItem>
                        <SelectItem value="luxury">Luxury</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <FormField
                    control={form.control}
                    name="notes"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Notes</FormLabel>
                        <FormControl>
                          <Textarea placeholder="Any special requests..." {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <Button type="submit">Submit</Button>
                </form>
              </Form>
            </CardContent>
          </Card>
        </Section>

        {/* Data Table */}
        <Section title="Data Table">
          <DataTable
            columns={carColumns}
            data={sampleCars}
            searchKey="make"
            searchPlaceholder="Filter by make..."
          />
        </Section>

        {/* Tabs */}
        <Section title="Tabs">
          <Tabs defaultValue="overview">
            <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="analytics">Analytics</TabsTrigger>
              <TabsTrigger value="settings">Settings</TabsTrigger>
            </TabsList>
            <TabsContent value="overview">
              <Card>
                <CardHeader>
                  <CardTitle>Overview</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">This is the overview tab content.</p>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="analytics">
              <Card>
                <CardHeader>
                  <CardTitle>Analytics</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">This is the analytics tab content.</p>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="settings">
              <Card>
                <CardHeader>
                  <CardTitle>Settings</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">This is the settings tab content.</p>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </Section>

        {/* Dialogs */}
        <Section title="Dialogs & Modals">
          <div className="flex flex-wrap gap-3">
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">Open Dialog</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Edit Car Details</DialogTitle>
                  <DialogDescription>
                    Make changes to the car information below.
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <Label>Make</Label>
                    <Input defaultValue="Toyota" />
                  </div>
                  <div className="space-y-2">
                    <Label>Model</Label>
                    <Input defaultValue="Camry" />
                  </div>
                </div>
                <DialogFooter>
                  <Button type="submit" onClick={() => toast.success("Changes saved!")}>
                    Save changes
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>

            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="destructive">
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete Car
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This action cannot be undone. This will permanently delete the
                    car from the fleet.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction onClick={() => toast.error("Car deleted!")}>
                    Delete
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>

            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline">
                  <Info className="mr-2 h-4 w-4" />
                  Popover
                </Button>
              </PopoverTrigger>
              <PopoverContent>
                <div className="space-y-2">
                  <h4 className="font-medium">Quick Info</h4>
                  <p className="text-sm text-muted-foreground">
                    This is a popover with additional information.
                  </p>
                </div>
              </PopoverContent>
            </Popover>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline">
                  Menu
                  <ChevronDown className="ml-2 h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuLabel>Actions</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => toast.info("View clicked")}>View</DropdownMenuItem>
                <DropdownMenuItem onClick={() => toast.info("Edit clicked")}>Edit</DropdownMenuItem>
                <DropdownMenuItem onClick={() => toast.info("Export clicked")}>Export</DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="text-destructive">Delete</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </Section>

        {/* Toast Notifications */}
        <Section title="Toast Notifications">
          <div className="flex flex-wrap gap-3">
            <Button variant="outline" onClick={() => toast.success("Operation completed successfully!")}>
              <CheckCircle className="mr-2 h-4 w-4" />
              Success Toast
            </Button>
            <Button variant="outline" onClick={() => toast.error("Something went wrong!")}>
              <AlertCircle className="mr-2 h-4 w-4" />
              Error Toast
            </Button>
            <Button variant="outline" onClick={() => toast.info("Here is some information.")}>
              <Info className="mr-2 h-4 w-4" />
              Info Toast
            </Button>
            <Button variant="outline" onClick={() => toast("Default notification")}>
              Default Toast
            </Button>
          </div>
        </Section>

        {/* Alerts */}
        <Section title="Alerts">
          <div className="space-y-4">
            <Alert>
              <Info className="h-4 w-4" />
              <AlertTitle>Information</AlertTitle>
              <AlertDescription>
                This is an informational alert with default styling.
              </AlertDescription>
            </Alert>
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>
                Something went wrong. Please try again later.
              </AlertDescription>
            </Alert>
          </div>
        </Section>

        {/* Skeletons */}
        <Section title="Skeleton Loading">
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <Skeleton className="h-12 w-12 rounded-full" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-[250px]" />
                <Skeleton className="h-4 w-[200px]" />
              </div>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              {[1, 2, 3].map((i) => (
                <Card key={i}>
                  <CardHeader>
                    <Skeleton className="h-4 w-[120px]" />
                    <Skeleton className="h-3 w-[80px]" />
                  </CardHeader>
                  <CardContent>
                    <Skeleton className="h-8 w-[60px]" />
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </Section>

        {/* Loading Spinner */}
        <Section title="Loading Spinner">
          <div className="flex items-end gap-8">
            <div className="text-center">
              <LoadingSpinner size="sm" />
              <p className="mt-2 text-sm text-muted-foreground">Small</p>
            </div>
            <div className="text-center">
              <LoadingSpinner size="md" />
              <p className="mt-2 text-sm text-muted-foreground">Medium</p>
            </div>
            <div className="text-center">
              <LoadingSpinner size="lg" />
              <p className="mt-2 text-sm text-muted-foreground">Large</p>
            </div>
          </div>
        </Section>

        {/* Empty State */}
        <Section title="Empty State">
          <Card>
            <CardContent className="pt-6">
              <EmptyState
                title="No bookings found"
                description="There are no bookings matching your filters. Try adjusting your search or create a new booking."
                actionLabel="Create Booking"
                onAction={() => toast.info("Create booking clicked!")}
              />
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <EmptyState
                icon={Search}
                title="No search results"
                description="We couldn't find any cars matching your query."
              />
            </CardContent>
          </Card>
        </Section>
      </div>
    </div>
  );
}
