import { AtSign, KeyIcon, Eye, EyeOff } from "lucide-react";
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { AuthForm } from "~/components/features/auth/auth-form";
import type { Route } from "../+types";
import { APP_META, DOCUMENT_META } from "~/constants/strings";

export function meta({}: Route.MetaArgs) {
  return [
    { title: `Sign in - ${APP_META.name}` },
    {
      name: "description",
      content: DOCUMENT_META.default,
    },
  ];
}


export default function SignIn() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [validationError, setValidationError] = useState("");

  const { mutate, isPending } = useMutation({
    mutationFn: async () => ({}),
    onSuccess: () => navigate("/"),
    onError: (error) => toast.error(error?.message),
  });

  useEffect(() => setValidationError(""), [email, password]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!email || !password) {
      setValidationError("Email and password are required");
      return;
    }
    setValidationError("");
    mutate();
  };

  return (
    <AuthForm
      title="Sign in"
      subtitle="Welcome back!"
      googleAction="Sign in"
      submitLabel="Sign in"
      onSubmit={handleSubmit}
      isSubmitting={isPending}
      validationError={validationError}
      fields={[
        {
          key: "email",
          element: (
            <div className="flex items-center gap-2 border rounded-md focus-within:ring focus-within:ring-primary overflow-hidden">
              <span className="bg-border/50 p-3">
                <AtSign className="size-4 text-muted-foreground" />
              </span>
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="flex-1 py-2 outline-none text-sm"
              />
            </div>
          ),
        },
        {
          key: "password",
          element: (
            <>
              <div className="flex items-center gap-2 border rounded-md focus-within:ring focus-within:ring-primary overflow-hidden">
                <span className="bg-border/50 p-3">
                  <KeyIcon className="size-4 text-muted-foreground" />
                </span>
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="flex-1 py-2 outline-none text-sm"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="p-3"
                >
                  {showPassword ? (
                    <Eye className="size-4 text-muted-foreground" />
                  ) : (
                    <EyeOff className="size-4 text-muted-foreground" />
                  )}
                </button>
              </div>
              <div className="mt-1 text-xs text-muted-foreground text-end">
                <Link to="/forgot-password" className="hover:underline">
                  Forgot password?
                </Link>
              </div>
            </>
          ),
        },
      ]}
      footer={
        <div className="text-center text-sm font-light text-muted-foreground font-brand">
          Don&apos;t have an account?{" "}
          <Link to="/sign-up" className="hover:underline hover:text-foreground">
            Sign up
          </Link>
        </div>
      }
    />
  );
}
