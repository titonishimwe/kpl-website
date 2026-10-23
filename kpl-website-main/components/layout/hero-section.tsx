import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import { Input } from "@/components/ui/input";
import { SearchIcon } from "lucide-react";
import { SearchCatalog } from "../seach-catalog";

export default function HeroSection(){
    return (
        <section className="flex justify-center items-center-safe w-full h-[350px] md:h-[550px] bg-[url('/images/bg/kplfront.jpg')] bg-cover bg-center">
          <div className="flex justify-center items-center w-full bg-secondary/50 h-10 md:h-20 p-1 md:p-2.5">
            <a className="w-1/3 md:w-1/6 lg:w-1/6 h-8 md:h-12 flex justify-between items-center  bg-accent text-white font-semibold rounded hover:bg-primary transition-colors uppercase md:text-lg lg:text-xl" href="https://library.kplonline.org/" target="_blank" rel="noopener noreferrer">
              <p className="text-center w-full">Catalog</p>
            </a>
            <SearchCatalog/>
          </div>
        </section>
    )   
}