import { APP_META } from "~/constants/strings";

export default function Footer() {
  return (
    <footer className="border-t border-foreground dark:border-border w-full flex items-center">
      <div className="w-full max-w-7xl mx-auto h-full border-x border-foreground dark:border-border px-4 flex justify-between items-center gap-4">
        <div className="w-full max-w-xl mx-auto  py-16 flex flex-wrap justify-between gap-8">
          <div className="flex-1 flex flex-col items-start">
            <img src="/logo.png" className="size-7" />
            <span className="text-base font-brand">
              {APP_META.name.toLowerCase()}
            </span>
            <span className="text-xs text-muted-foreground">
              &copy;&nbsp;{new Date().getFullYear()}&nbsp;{APP_META.parent}
              ,&nbsp;
              {APP_META.address}
            </span>
          </div>

          <div className="flex flex-wrap gap-8">
            <div className="flex flex-col items-start space-y-2">
              <a
                href="/about"
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                About
              </a>
              <a
                href="/careers"
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Careers
              </a>
              <a
                href="/help"
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Help
              </a>
            </div>

            <div className="flex flex-col items-start space-y-2">
              <a
                href="/terms"
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Terms of Service
              </a>
              <a
                href="/privacy"
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Privacy Policy
              </a>
              <a
                href="/contact"
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Contact Us
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
