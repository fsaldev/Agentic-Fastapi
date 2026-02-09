export type CarCategory = "economy" | "standard" | "luxury" | "suv";

export type CarStatus = "available" | "rented" | "maintenance";

export interface Car {
  id: string;
  make: string;
  model: string;
  year: number;
  license_plate: string;
  daily_rate: number;
  category: CarCategory;
  status: CarStatus;
  created_at: string;
}

export interface CarCreate {
  make: string;
  model: string;
  year: number;
  license_plate: string;
  daily_rate: number;
  category?: CarCategory;
}

export interface CarUpdate {
  make?: string;
  model?: string;
  year?: number;
  license_plate?: string;
  daily_rate?: number;
  category?: CarCategory;
  status?: CarStatus;
}

export interface CarFilters {
  status?: CarStatus;
  category?: CarCategory;
}

export interface CarAvailability {
  available: boolean;
}
