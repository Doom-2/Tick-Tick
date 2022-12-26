import { User } from "../../../models/user";

export function getInitials(user: User): string {
  if (!user.first_name && !user.last_name) {
    return user.username.substring(0, 2);
  }

  let res = '';

  if (user.first_name) {
    res += user.first_name.substring(0, 1);
  }

  if (user.last_name) {
    res += user.last_name.substring(0, 1);
  }

  return res;
}
