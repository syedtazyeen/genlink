import { ArrowLeft } from "lucide-react";
import { Link } from "react-router";
import { UIButton } from "~/components/ui/button";

type FieldProps = {
  key: string;
  element: React.ReactNode;
};

type AuthFormProps = {
  title: string;
  subtitle: string;
  googleAction: string;
  fields: FieldProps[];
  validationError?: string;
  submitLabel: string;
  isSubmitting?: boolean;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  footer: React.ReactNode;
};

export function AuthForm({
  title,
  subtitle,
  googleAction,
  fields,
  validationError,
  submitLabel,
  isSubmitting,
  onSubmit,
  footer,
}: AuthFormProps) {
  return (
    <div className="border w-96 p-6 rounded-md space-y-6 bg-card">
      <img src="/logo.png" alt="Logo" className="size-7" />
      <div>
        <h1 className="text-2xl font-brand">{title}</h1>
        <p className="text-sm text-muted-foreground font-brand font-light">
          {subtitle}
        </p>
      </div>

      <UIButton variant="secondary" brand>
        {googleAction} with Google
      </UIButton>

      <p className="text-muted-foreground font-brand text-xs text-center">or</p>

      <form onSubmit={onSubmit} className="space-y-3">
        {fields.map(({ key, element }) => (
          <div key={key}>{element}</div>
        ))}

        {validationError && (
          <p className="text-destructive-foreground text-xs text-center">
            {validationError}
          </p>
        )}

        <UIButton className="mb-4" type="submit" isLoading={isSubmitting} brand>
          {submitLabel}
        </UIButton>

        {footer}

        <div className="mt-4 flex justify-center items-center gap-1 text-xs text-muted-foreground/50 font-brand">
          <ArrowLeft className="size-4" />
          <Link to="/" className="hover:underline">
            Back to home
          </Link>
        </div>
      </form>
    </div>
  );
}
