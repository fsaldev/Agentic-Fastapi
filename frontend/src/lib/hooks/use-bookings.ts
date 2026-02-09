import useSWR, { useSWRConfig } from "swr";
import { api } from "@/lib/api/client";
import type { Booking, BookingCreate, BookingFilters } from "@/types/booking";

function buildBookingQueryString(filters?: BookingFilters): string {
  if (!filters) return "";
  const params = new URLSearchParams();
  if (filters.status) params.set("status", filters.status);
  if (filters.car_id) params.set("car_id", filters.car_id);
  if (filters.customer_id) params.set("customer_id", filters.customer_id);
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

export function useBookings(filters?: BookingFilters) {
  const key = `/bookings${buildBookingQueryString(filters)}`;
  const { data, error, isLoading, mutate } = useSWR<Booking[]>(key);

  return {
    bookings: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useBooking(id: string | null) {
  const { data, error, isLoading, mutate } = useSWR<Booking>(
    id ? `/bookings/${id}` : null
  );

  return {
    booking: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useBookingMutations() {
  const { mutate } = useSWRConfig();

  async function invalidateBookings() {
    await mutate(
      (key: string) =>
        typeof key === "string" && key.startsWith("/bookings"),
      undefined,
      { revalidate: true }
    );
  }

  async function createBooking(data: BookingCreate): Promise<Booking> {
    const booking = await api.post<Booking>("/bookings", data);
    await invalidateBookings();
    return booking;
  }

  async function pickupBooking(id: string): Promise<Booking> {
    const booking = await api.post<Booking>(`/bookings/${id}/pickup`);
    await mutate(`/bookings/${id}`, booking, { revalidate: false });
    await invalidateBookings();
    return booking;
  }

  async function returnBooking(id: string): Promise<Booking> {
    const booking = await api.post<Booking>(`/bookings/${id}/return`);
    await mutate(`/bookings/${id}`, booking, { revalidate: false });
    await invalidateBookings();
    // Also invalidate cars since car status changes on return
    await mutate(
      (key: string) => typeof key === "string" && key.startsWith("/cars"),
      undefined,
      { revalidate: true }
    );
    return booking;
  }

  async function cancelBooking(id: string): Promise<Booking> {
    const booking = await api.post<Booking>(`/bookings/${id}/cancel`);
    await mutate(`/bookings/${id}`, booking, { revalidate: false });
    await invalidateBookings();
    return booking;
  }

  return { createBooking, pickupBooking, returnBooking, cancelBooking };
}
