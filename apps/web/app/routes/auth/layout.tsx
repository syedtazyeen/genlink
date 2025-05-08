import { Outlet } from "react-router";
import Background from "~/components/common/Background";

export default function AuthLayout() {
  return (
    <main className="w-full min-h-screen flex items-center justify-center">
      <Background />
      <Outlet/>
    </main>
  );
}
