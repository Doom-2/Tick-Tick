import { AbstractControl, FormGroup } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { format } from 'date-fns'

export type ApiErrors = Record<string, string[]>;

export function setErrorToForm(form: FormGroup, errors: ApiErrors): void {
  Object.entries(errors).forEach(([field, errorList]) => {
    setErrorToControl(form.controls[field], errorList);
  })
}

export function setErrorToControl(control: AbstractControl, errors: string[]): void {
  const errorMap = errors.reduce((obj, value, index) => {
    // @ts-ignore
    obj['apiError' + index] = value;
    return obj;
  }, {});
  control.setErrors(errorMap, { emitEvent: true });
}

export function getErrors(
  httpError: HttpErrorResponse,
  availableKeys: string[] | null = null,
): { nonFieldErrors: string[], apiErrors: ApiErrors } {
  if (httpError.status === 403 && !httpError?.error) {
    return {
      apiErrors: {},
      nonFieldErrors: ['Forbidden']
    }
  }

  if (httpError.status === 405) {
    return {
      apiErrors: {},
      nonFieldErrors: ['Method not allowed']
    }
  }

  if (httpError.status === 500 || !httpError?.error) {
    return {
      apiErrors: {},
      nonFieldErrors: ['Server error 500']
    }
  }

  const { non_field_errors, detail, ...apiErrors } = httpError.error;
  const nonFieldErrors = non_field_errors || [];

  if (availableKeys) {
    Object.entries(apiErrors)
      .filter(([key, value]) => !availableKeys.includes(key))
      .forEach(([key, value]) => {
        nonFieldErrors.push(...(value as string[]))
      })
  }

  if (detail) {
    nonFieldErrors.push(detail);
  }

  return {
    apiErrors: apiErrors || {},
    nonFieldErrors,
  }
}

export function prepareDate(date: Date | null | string): string | null {
  if (!date) {
    return null;
  }

  if (typeof date === 'string') {
    return date;
  }

  return format(date, 'yyyy-MM-dd');
}
