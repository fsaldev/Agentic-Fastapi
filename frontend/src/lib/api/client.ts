import { config } from "@/config";
import { ApiRequestError } from "@/types/api";

const BASE_URL = `${config.apiUrl}/api/v1`;

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new ApiRequestError(
      response.status,
      body.detail || response.statusText,
      body.detail
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export const api = {
  async get<T>(path: string): Promise<T> {
    const response = await fetch(`${BASE_URL}${path}`);
    return handleResponse<T>(response);
  },

  async post<T>(path: string, body?: unknown): Promise<T> {
    const response = await fetch(`${BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    });
    return handleResponse<T>(response);
  },

  async put<T>(path: string, body: unknown): Promise<T> {
    const response = await fetch(`${BASE_URL}${path}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    return handleResponse<T>(response);
  },

  async delete(path: string): Promise<void> {
    const response = await fetch(`${BASE_URL}${path}`, {
      method: "DELETE",
    });
    return handleResponse<void>(response);
  },
};

export function fetcher<T>(path: string): Promise<T> {
  return api.get<T>(path);
}
