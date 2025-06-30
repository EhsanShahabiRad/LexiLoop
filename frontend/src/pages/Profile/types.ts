import { z } from "zod";
import { profileSchema } from "./validationSchema";

export type ProfileFormData = z.infer<typeof profileSchema>;
