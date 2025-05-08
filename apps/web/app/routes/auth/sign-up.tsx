import { AtSign, KeyIcon, User, Eye, EyeOff } from "lucide-react";
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { AuthForm } from "~/components/features/auth/auth-form";
import { APP_META, DOCUMENT_META } from "~/constants/strings";
import type { Route } from "../+types";
import { checkPasswordStrength } from "~/lib/utils";

export function meta({}: Route.MetaArgs) {
  return [
    { title: `Sign up - ${APP_META.name}` },
    {
      name: "description",
      content: DOCUMENT_META.default,
    },
  ];
}

export default function SignUp() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [validationError, setValidationError] = useState("");

  const { mutate, isPending } = useMutation({
    mutationFn: async () => ({}),
    onSuccess: () => navigate("/"),
    onError: (error) => toast.error(error?.message),
  });

  useEffect(() => setValidationError(""), [name, email, password]);

  const { strength, message } = checkPasswordStrength(password);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!name || !email || !password) {
      setValidationError("All fields are required");
      return;
    }
    setValidationError("");
    mutate();
  };

  return (
    <AuthForm
      title="Create account"
      subtitle="Let’s get started"
      googleAction="Sign up"
      submitLabel="Create account"
      onSubmit={handleSubmit}
      isSubmitting={isPending}
      validationError={validationError}
      fields={[
        {
          key: "name",
          element: (
            <div className="flex items-center gap-2 border rounded-md focus-within:ring focus-within:ring-primary overflow-hidden">
              <span className="bg-border/50 p-3">
                <User className="size-4 text-muted-foreground" />
              </span>
              <input
                type="text"
                placeholder="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="flex-1 py-2 outline-none text-sm"
              />
            </div>
          ),
        },
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
              <div className="mt-2 mb-4 space-y-1 text-xs text-muted-foreground font-brand">
                <div className="flex items-center gap-2">
                  {Array.from({ length: 3 }).map((_, i) => {
                    let barColor = "bg-border/50";
                    if (strength === "weak" && i === 0)
                      barColor = "bg-red-600/50";
                    if (strength === "medium" && i <= 1)
                      barColor = "bg-yellow-600/50";
                    if (strength === "strong") barColor = "bg-green-600/50";

                    return (
                      <div key={i} className={`flex-1 h-0.5 ${barColor}`} />
                    );
                  })}
                </div>
                <p className="text-muted-foreground text-xs h-5">{message}</p>
              </div>
            </>
          ),
        },
      ]}
      footer={
        <div className="text-center text-sm font-light text-muted-foreground font-brand">
          Already have an account?{" "}
          <Link to="/sign-in" className="hover:underline hover:text-foreground">
            Sign in
          </Link>
        </div>
      }
    />
  );
}
