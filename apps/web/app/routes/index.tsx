import Background from "~/components/features/landing/background";
import type { Route } from "./+types";
import { APP_META, DOCUMENT_META } from "~/constants/strings";
import Header from "~/components/features/landing/header";
import Hero from "~/components/features/landing/hero";
import About from "~/components/features/landing/about";
import Pricing from "~/components/features/landing/pricing";
import Footer from "~/components/features/landing/footer";

export function meta({}: Route.MetaArgs) {
  return [
    { title: `${APP_META.name} - Your Thinking Workspace` },
    {
      name: "description",
      content: DOCUMENT_META.default,
    },
  ];
}
export default function Home() {
  return (
    <div className="w-full">
      <Background />
      <Header />
      <main className="w-full">
        <div className="pb-40 max-w-7xl mx-auto border-x border-foreground dark:border-border">
          <Hero />
          <About />
          <Pricing />
        </div>
      </main>
      <Footer />
    </div>
  );
}
