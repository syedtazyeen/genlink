import React from "react";
import { Loader } from "lucide-react";
import { cn } from "~/lib/utils";

type UIButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "default" | "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
  brand?: boolean;
  isLoading?: boolean;
};

const baseStyles =
  "rounded-md transition text-sm w-full transition duration-100";

const variantStyles = {
  default:
    "bg-primary/10 border border-primary text-primary hover:bg-primary hover:text-primary-foreground data-[loading=true]:pointer-events-none data-[loading=true]:bg-primary data-[loading=true]:text-primary-foreground data-[loading=true]:opacity-50",
  primary: "bg-primary text-primary-foreground hover:bg-primary/90",
  secondary:
    "border bg-border text-foreground hover:bg-foreground hover:text-background",
  outline: "border border-border text-foreground hover:bg-border/20",
  ghost: "bg-transparent text-foreground hover:bg-border/30",
};

const sizeStyles = {
  sm: "px-3 h-8 text-sm",
  md: "px-4 h-10 text-sm",
  lg: "px-5 h-12 text-base",
};

export const UIButton: React.FC<UIButtonProps> = ({
  variant = "default",
  size = "md",
  brand = false,
  className,
  isLoading,
  children,
  ...props
}) => {
  return (
    <button
    data-loading={isLoading}
      className={cn(
        baseStyles,
        variantStyles[variant],
        sizeStyles[size],
        brand && "font-brand",
        className
      )}
      {...props}
    >
      {isLoading ? <Loader className="animate-spin mx-auto"/> : children}
    </button>
  )
};
