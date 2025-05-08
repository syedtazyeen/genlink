import { MoveRight } from "lucide-react";
import { Link } from "react-router";

export default function Hero() {
  return (
    <div
      id="hero"
      className="px-4 min-h-[calc(100dvh-5rem)] pt-40 text-center font-brand"
    >
      <h1 className="text-5xl leading-tight max-w-2xl mx-auto tracking-tighter">
        Think, note, and move fast.
      </h1>
      <p className="mt-2 text-lg font-light max-w-3xl mx-auto text-muted-foreground tracking-wider">
        Manage tasks, sketch ideas, draft reports, take notes, learn on the fly,
        and stay in flow — all in one agentic workspace built for momentum.
      </p>
      <div className="mt-16">
        <Link
          to={"/sign-in"}
          className="group flex items-center gap-2 w-fit mx-auto text-lg bg-primary/10 border border-primary text-primary px-6 py-2 rounded-md shadow-lg shadow-primary/10 hover:bg-primary hover:text-primary-foreground transition duration-100"
        >
          Get started{" "}
          <MoveRight className="group-hover:translate-x-1 transition duration-100" />
        </Link>
      </div>
      <div className="mt-24 text-center flex items-center justify-center">
        <p className="text-muted-foreground border-b border-dashed p-1">
          Loved by <span className="text-primary">10k+</span> users
        </p>
      </div>
    </div>
  );
}
