import { useEffect, useRef } from "react";
import { Link } from "react-router";
import { APP_META } from "~/constants/strings";

export default function Header() {
  const headerRef = useRef<HTMLHeadElement | null>(null);

  useEffect(() => {
    const header = headerRef.current;
    if (!header) return;

    const updateHeaderOnScroll = () => {
      if (window.scrollY > 0) {
        header.setAttribute("data-scrolled", "true");
      } else {
        header.setAttribute("data-scrolled", "false");
      }
    };

    window.addEventListener("scroll", updateHeaderOnScroll);
    updateHeaderOnScroll();

    return () => window.removeEventListener("scroll", updateHeaderOnScroll);
  }, []);

  return (
    <header
      ref={headerRef}
      className="border-b border-foreground dark:border-border w-full h-16 flex items-center sticky top-0 z-50 transition-all duration-300 backdrop-blur-0 bg-background/0 data-[scrolled=true]:backdrop-blur-md data-[scrolled=true]:bg-background/95"
    >
      <div className="w-full max-w-7xl mx-auto h-full border-x border-foreground dark:border-border px-4 flex justify-between items-center gap-4">
        <div className="font-brand flex items-center gap-2">
          <img src="/logo.png" className="size-7" />
          <span className="text-2xl font-light tracking-tight">
            {APP_META.name.toLowerCase()}
          </span>
        </div>
        <div className="text-muted-foreground tracking-wide flex items-center gap-4">
          <Link
            to={"#about"}
            className="text-sm hover:text-foreground transition"
          >
            Our Story
          </Link>
          <Link
            to={"#pricing"}
            className="text-sm hover:text-foreground transition"
          >
            Pricing
          </Link>
          <Link
            to={"/sign-in"}
            className="text-sm bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/95 transition"
          >
            Sign in
          </Link>
        </div>
      </div>
    </header>
  );
}
