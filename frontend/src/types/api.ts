export interface ApiError {
  status: number;
  message: string;
  detail?: string;
}

export class ApiRequestError extends Error {
  status: number;
  detail?: string;

  constructor(status: number, message: string, detail?: string) {
    super(message);
    this.name = "ApiRequestError";
    this.status = status;
    this.detail = detail;
  }
}
