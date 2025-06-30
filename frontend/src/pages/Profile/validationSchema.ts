import { z } from "zod";

export const profileSchema = z.object({
  username: z
    .string()
    .min(5, "Username must be at least 5 characters")
    .max(20, "Username must be at most 20 characters")
    .regex(
      /^[a-zA-Z0-9](?!.*[_.-]{2})[a-zA-Z0-9_.-]*[a-zA-Z0-9]$/,
      "Username must be 5–20 characters, start/end with letter/number, and contain only letters, numbers, dots, underscores or dashes (no consecutive symbols)"
    ),
  name: z
    .string()
    .min(2, { message: "Name must be at least 2 characters." })
    .max(50, { message: "Name must be less than 50 characters." })
    .regex(/^[\p{L} ]+$/u, {
      message: "Name can only contain letters and spaces.",
    }),
  active_language_pair_id: z
    .string()
    .min(1, "Language pair is required")
    .regex(/^\d+$/, "Must be a valid numeric ID"),
  email: z.string().email("Invalid email address"),
});
