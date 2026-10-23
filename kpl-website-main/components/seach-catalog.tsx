"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ButtonGroup } from "@/components/ui/button-group";
import { SearchIcon } from "lucide-react";

const KOHA_SEARCH_URL =
    "https://library.kplonline.org/cgi-bin/koha/opac-search.pl";

export const SearchCatalog = () => {
    const [query, setQuery] = useState("");

    const sanitizeQuery = (input: string) => {
        return input
            .trim()
            .replace(/\s+/g, " ")
            .replace(/[^\w\s\-']/g, "")
            .slice(0, 50);
    };

    const handleSearch = () => {
        const sanitized = sanitizeQuery(query);

        if (!sanitized) return;

        const params = new URLSearchParams({ q: sanitized });
        window.location.href = `${KOHA_SEARCH_URL}?${params.toString()}`;
    };

    return (
        <ButtonGroup className="ml-4 lg:w-1/4 flex justify-between items-center">
            <label htmlFor="search" className="sr-only">
                Search the catalog
            </label>

            <Input
                id="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                placeholder="Search the catalog..."
                className="w-11/12 py-3 bg-background focus-visible:ring-0
                   md:text-lg lg:text-xl h-8 md:h-12"
            />

            <Button
                onClick={handleSearch}
                className="bg-secondary h-8 md:h-12"
                aria-label="Search"
            >
                <SearchIcon />
            </Button>
        </ButtonGroup>
    );
};
