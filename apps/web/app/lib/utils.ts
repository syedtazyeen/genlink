import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function checkPasswordStrength(password: string): {
  strength: "none" | "weak" | "medium" | "strong";
  message: string;
} {
  let strength: "none" | "weak" | "medium" | "strong" = "none";

  if (password.length === 0) {
    strength = "none";
  } else if (password.length < 8) {
    strength = "weak";
  } else if (password.length < 12) {
    strength = "medium";
  } else {
    strength = "strong";
  }

  const messageMap: Record<typeof strength, string> = {
    none: "",
    weak: "Too short",
    medium: "Okay",
    strong: "Good",
  };

  return {
    strength,
    message: messageMap[strength],
  };
}
