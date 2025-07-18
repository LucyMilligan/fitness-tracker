"use client";
import Image from "next/image";
import Link from "next/link";
import { useState } from "react";

export default function Home() {
  return (
    <>
      <main>
        <p className="text-[45px] text-center py-8 font-semibold font-[family-name:var(--font-geist-mono)]">
          Home
        </p>
        <p className="text-[16px] text-black text-center pb-5">
          Welcome to the fitness tracker app!
        </p>
        <p className="text-[16px] text-black text-center py-5">
          Select one of the options below to track and visualise your activities
          and fitness levels.
        </p>
        {/* <ol className="list-inside list-decimal text-sm/8 text-center pl-5">
          <li>
            Enter activity data
          </li>
          <li>
            View and filter activity data
          </li>
          <li>
            Visualise activity data and monitor fitness levels
          </li>
        </ol> */}

        <div className="flex gap-6 items-center justify-center flex-col py-10">
          <Link
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
            href="create_user"
          >
            Create User
          </Link>
          <Link
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
            href="enter_data"
          >
            Enter Activity Data
          </Link>
          <Link
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
            href="view_data"
          >
            View Activity Data
          </Link>
          {/* <Link
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
            href="update_data"
          >
            Update Activity Data
          </Link> */}
          <Link
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
            href="visualise_data"
          >
            Visualise Data
          </Link>
        </div>
      </main>
    </>
  );
}

//     <div className="grid grid-rows-[10px_1fr_10px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
//       <main className="flex flex-col gap-[20px] row-start-2 items-center">
//         <p className="text-[50px] font-semibold font-[family-name:var(--font-geist-mono)]">Fitness Tracker</p>
// <div className="flex gap-8 flex-row sm:flex-row py-2">
//   <Image
//     className="justify-center"
//     src="/swimming.svg"
//     alt="Fitness Tracker logo"
//     width={60}
//     height={30}
//     priority
//   />
//   <Image
//     className="justify-center"
//     src="/cycling.svg"
//     alt="Fitness Tracker logo"
//     width={50}
//     height={30}
//     priority
//   />
//   <Image
//     className="justify-center"
//     src="/running.svg"
//     alt="Fitness Tracker logo"
//     width={60}
//     height={30}
//     priority
//   />
// </div>
//   <p className="text-[15px] text-black font-[family-name:var(--font-geist-mono)]">Welcome to the fitness tracker app! Here you'll be able to...</p>
//   <ol className="list-inside list-decimal text-sm/8 text-center font-[family-name:var(--font-geist-mono)] pl-5">
//     <li className="tracking-[-.01em]">
//       Enter activity data
//     </li>
//     <li className="tracking-[-.01em]">
//       View and filter activity data
//     </li>
//     <li className="tracking-[-.01em]">
//       Visualise activity data and monitor fitness levels
//     </li>
//   </ol>

//   <div className="flex gap-6 items-center flex-col sm:flex-row py-6">
//     {/* <a
//       className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
//       href="dashboard"
//       rel="noopener noreferrer"
//     >
//       Let's go!
//     </a> */}
//     <Link
//       className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
//       href="enter_data"
//       rel="noopener noreferrer"
//     >
//       Enter Activity Data
//     </Link>
//     <Link
//       className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
//       href="view_data"
//       rel="noopener noreferrer"
//     >
//       View Activity Data
//     </Link>
//     <Link
//       className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-slate-700 text-white gap-2 hover:bg-teal-600 font-normal text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto"
//       href="visualise_data"
//       rel="noopener noreferrer"
//     >
//       Visualise Data
//     </Link>
//   </div>
// </main>
// <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
//   <p
//     className="flex items-center gap-2"
//   >
//     © 2025 by Lucy Milligan
//   </p>
//   <a
//     className="flex items-center gap-2 hover:underline hover:underline-offset-4"
//     href="https://www.linkedin.com/in/lucy-milligan-888491150/"
//     target="_blank"
//     rel="noopener noreferrer"
//   >
//     <Image
//       aria-hidden
//       src="/linkedin.svg"
//       alt="LinkedIn icon"
//       width={16}
//       height={16}
//     />
//     Lucy's LinkedIn
//   </a>
//   <a
//     className="flex items-center gap-2 hover:underline hover:underline-offset-4"
//     href="https://github.com/LucyMilligan"
//     target="_blank"
//     rel="noopener noreferrer"
//   >
//     <Image
//       aria-hidden
//       src="/github.svg"
//       alt="GitHub icon"
//       width={16}
//       height={16}
//     />
//     Other projects
//   </a>
// </footer>
//     </div>
//   );
// }
