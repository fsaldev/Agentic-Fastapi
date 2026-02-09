export interface Customer {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  driver_license: string;
  created_at: string;
}

export interface CustomerCreate {
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  driver_license: string;
}

export interface CustomerUpdate {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  driver_license?: string;
}
