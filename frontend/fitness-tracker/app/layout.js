import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Image from "next/image";
import Link from "next/link";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Fitness tracker app",
};


export default function RootLayout( {children}) {
  return (
    <html lang="en">
      <body
        className={`${geistMono.variable} ${geistSans.variable} bg-cyan-500/40 text-black items-center justify-items-center gap-5`}
      >
        <header className="bg-cyan-500/70 w-full justify-items-center">
          <h1 className="text-[35px] font-semibold font-[family-name:var(--font-geist-mono)]">Fitness Tracker</h1>
          <div className="justify-center flex gap-6 flex-row sm:flex-row py-2">
              <Image
                className="justify-center"
                src="/swimming.svg"
                alt="Fitness Tracker logo"
                width={40}
                height={20}
                priority
              />
              <Image
                className="justify-center"
                src="/cycling.svg"
                alt="Fitness Tracker logo"
                width={35}
                height={20}
                priority
              />
              <Image
                className="justify-center"
                src="/running.svg"
                alt="Fitness Tracker logo"
                width={40}
                height={20}
                priority
              />
            </div>
        </header>
        <main>{children}</main>
        <footer className="flex gap-[24px] flex-wrap py-5 mt-15 bg-cyan-500/70 w-full justify-center"> {/*doesn't look consistent with header on small page*/}
          <p
            className="flex gap-2"
          >
            © 2025 by Lucy Milligan
          </p>
          <Link
            className="flex gap-2 hover:underline hover:underline-offset-4"
            href="/"
          >
            <Image
              aria-hidden
              src="/homepage.svg"
              alt="Home icon"
              width={18}
              height={18}
            />
            Home
          </Link>
          <a
            className="flex gap-2 hover:underline hover:underline-offset-4"
            href="https://www.linkedin.com/in/lucy-milligan-888491150/"
            target="_blank"
            rel="noopener noreferrer" //used for security when linking to external sites
          >
            <Image
              aria-hidden
              src="/linkedin.svg"
              alt="LinkedIn icon"
              width={16}
              height={16}
            />
            Lucy's LinkedIn
          </a>
          <a
            className="flex gap-2 hover:underline hover:underline-offset-4"
            href="https://github.com/LucyMilligan"
            target="_blank"
            rel="noopener noreferrer" //used for security when linking to external sites
          >
            <Image
              aria-hidden
              src="/github.svg"
              alt="GitHub icon"
              width={16}
              height={16}
            />
            Other projects
          </a>
        </footer>
      </body>
    </html>
  );
}
