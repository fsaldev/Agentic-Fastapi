import useSWR, { useSWRConfig } from "swr";
import { api } from "@/lib/api/client";
import type {
  Car,
  CarCreate,
  CarUpdate,
  CarFilters,
  CarAvailability,
} from "@/types/car";

function buildCarQueryString(filters?: CarFilters): string {
  if (!filters) return "";
  const params = new URLSearchParams();
  if (filters.status) params.set("status", filters.status);
  if (filters.category) params.set("category", filters.category);
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

export function useCars(filters?: CarFilters) {
  const key = `/cars${buildCarQueryString(filters)}`;
  const { data, error, isLoading, mutate } = useSWR<Car[]>(key);

  return {
    cars: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useCar(id: string | null) {
  const { data, error, isLoading, mutate } = useSWR<Car>(
    id ? `/cars/${id}` : null
  );

  return {
    car: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useCarAvailability(
  carId: string | null,
  startDate: string | null,
  endDate: string | null
) {
  const key =
    carId && startDate && endDate
      ? `/cars/${carId}/availability?start_date=${startDate}&end_date=${endDate}`
      : null;

  const { data, error, isLoading } = useSWR<CarAvailability>(key);

  return {
    availability: data,
    isLoading,
    isError: error,
  };
}

export function useCarMutations() {
  const { mutate } = useSWRConfig();

  async function createCar(data: CarCreate): Promise<Car> {
    const car = await api.post<Car>("/cars", data);
    await mutate((key: string) => typeof key === "string" && key.startsWith("/cars"), undefined, { revalidate: true });
    return car;
  }

  async function updateCar(id: string, data: CarUpdate): Promise<Car> {
    const car = await api.put<Car>(`/cars/${id}`, data);
    await mutate(`/cars/${id}`, car, { revalidate: false });
    await mutate((key: string) => typeof key === "string" && key === "/cars" || (typeof key === "string" && key.startsWith("/cars?")), undefined, { revalidate: true });
    return car;
  }

  async function deleteCar(id: string): Promise<void> {
    await api.delete(`/cars/${id}`);
    await mutate((key: string) => typeof key === "string" && key.startsWith("/cars"), undefined, { revalidate: true });
  }

  return { createCar, updateCar, deleteCar };
}
