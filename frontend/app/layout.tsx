import "./globals.css";

export const metadata = {
  title: "Smart CV Optimizer",
  description: "ATS-friendly CV optimization and honest feedback",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  );
}
