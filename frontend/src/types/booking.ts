export type BookingStatus = "reserved" | "active" | "completed" | "cancelled";

export interface Booking {
  id: string;
  car_id: string;
  customer_id: string;
  start_date: string;
  end_date: string;
  actual_return_date: string | null;
  total_cost: number;
  status: BookingStatus;
  created_at: string;
}

export interface BookingCreate {
  car_id: string;
  customer_id: string;
  start_date: string;
  end_date: string;
}

export interface BookingFilters {
  status?: BookingStatus;
  car_id?: string;
  customer_id?: string;
}
