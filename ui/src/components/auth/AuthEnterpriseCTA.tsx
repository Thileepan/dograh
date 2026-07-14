// Enterprise call-to-action rendered inside the auth brand panel. Links out
// to the enterprise enquiry form. Shared by the Stack Auth handler and the
// local/OSS auth pages.

import { Button } from "@/components/ui/button";

const ENTERPRISE_ENQUIRY_URL =
  "https://fxk3ltckls6.typeform.com/to/YP0P1k1x?typeform-source=dcxworks.com";

export function AuthEnterpriseCTA() {
  return (
    <Button
      asChild
      variant="outline"
      className="w-full border-white/20 bg-white/5 text-zinc-100 hover:bg-white/10 hover:text-white"
    >
      <a href={ENTERPRISE_ENQUIRY_URL} target="_blank" rel="noopener noreferrer">
        Enterprise Enquiry
      </a>
    </Button>
  );
}
