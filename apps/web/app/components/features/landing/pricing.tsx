import { UIButton } from "~/components/ui/button";
import { cn } from "~/lib/utils";

type Plan = {
  title: string;
  features: React.ReactNode[];
  buttonLabel: string;
  popular?: boolean;
  disabled?: boolean;
  className?: string;
};

function ListItem({ children }: { children: React.ReactNode }) {
  return (
    <li className="flex items-center gap-2 text-muted-foreground text-sm font-light">
      <span className="text-primary">✓</span>
      {children}
    </li>
  );
}

function PlanCard({
  title,
  features,
  buttonLabel,
  popular,
  disabled,
  className = "",
}: Plan) {
  function getButtonVariant() {
    if (disabled) {
      return "outline";
    } else if (popular) {
      return "primary";
    } else {
      return "outline";
    }
  }

  function getCardClassName() {
    if (popular) {
      return "shadow-lg border-primary bg-primary/2 relative hover:shadow-primary/5";
    } else {
      return "bg-card hover:border-border";
    }
  }

  return (
    <div
      className={cn(
        `min-h-80 rounded-md p-6 flex flex-col justify-between border transition duration-300`,
        getCardClassName(),
        className
      )}
    >
      {popular && (
        <span className="bg-primary/60 absolute top-0 right-0 m-2 text-xs px-2 py-1 rounded-full">
          Popular
        </span>
      )}
      <div>
        <h3 className="text-lg mb-4">{title}</h3>
        <ul className="text-left space-y-2 mb-6">
          {features.map((feature, idx) => (
            <ListItem key={idx}>{feature}</ListItem>
          ))}
        </ul>
      </div>
      <UIButton disabled={disabled} variant={getButtonVariant()} brand>
        {buttonLabel}
      </UIButton>
    </div>
  );
}

export default function Pricing() {
  return (
    <div
      id="pricing"
      className="w-full max-w-5xl mx-auto py-20 text-center font-brand px-4"
    >
      <h1 className="text-4xl leading-tight max-w-lg mx-auto tracking-tighter">
        Pricing
      </h1>
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
        <PlanCard
          title="Free"
          buttonLabel="Start for Free"
          features={[
            "Up to 2 spaces",
            "Limited daily chat messages",
            "Limited library access",
            "Email & Notion integration",
          ]}
        />
        <PlanCard
          title="Premium"
          buttonLabel="Get Premium"
          popular
          features={[
            "Unlimited spaces",
            "Unlimited daily chat messages",
            "Invite collaborators",
            "Complete library access",
          ]}
        />
        <PlanCard
          title="Custom"
          buttonLabel="Contact Us"
          disabled
          features={[
            "Tailored solutions",
            "Priority support",
            "Advanced integrations",
          ]}
        />
      </div>
    </div>
  );
}
