import { HttpParams } from "@angular/common/http";

export function prepareHttpParams<T>(params: T): HttpParams {
  return new HttpParams({
    fromObject: Object.entries(params)
      .filter(([key, value]) => !!value)
      .reduce((obj, [key, value]) => ({
        ...obj,
        [key]: value,
      }), {})
  })
}
