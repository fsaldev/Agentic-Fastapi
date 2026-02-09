import useSWR, { useSWRConfig } from "swr";
import { api } from "@/lib/api/client";
import type { Customer, CustomerCreate, CustomerUpdate } from "@/types/customer";

export function useCustomers() {
  const { data, error, isLoading, mutate } = useSWR<Customer[]>("/customers");

  return {
    customers: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useCustomer(id: string | null) {
  const { data, error, isLoading, mutate } = useSWR<Customer>(
    id ? `/customers/${id}` : null
  );

  return {
    customer: data,
    isLoading,
    isError: error,
    mutate,
  };
}

export function useCustomerMutations() {
  const { mutate } = useSWRConfig();

  async function createCustomer(data: CustomerCreate): Promise<Customer> {
    const customer = await api.post<Customer>("/customers", data);
    await mutate("/customers", undefined, { revalidate: true });
    return customer;
  }

  async function updateCustomer(
    id: string,
    data: CustomerUpdate
  ): Promise<Customer> {
    const customer = await api.put<Customer>(`/customers/${id}`, data);
    await mutate(`/customers/${id}`, customer, { revalidate: false });
    await mutate("/customers", undefined, { revalidate: true });
    return customer;
  }

  async function deleteCustomer(id: string): Promise<void> {
    await api.delete(`/customers/${id}`);
    await mutate("/customers", undefined, { revalidate: true });
  }

  return { createCustomer, updateCustomer, deleteCustomer };
}
