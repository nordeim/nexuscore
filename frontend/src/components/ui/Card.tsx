/**
 * Card Component
 * Reusable card with header, body, footer
 */
import { ReactNode } from 'react';

interface CardProps {
    children: ReactNode;
    className?: string;
    hover?: boolean;
}

interface CardHeaderProps {
    children: ReactNode;
    className?: string;
}

interface CardBodyProps {
    children: ReactNode;
    className?: string;
}

interface CardFooterProps {
    children: ReactNode;
    className?: string;
}

export function Card({ children, className = '', hover = false }: CardProps) {
    return (
        <div
            className={`
        bg-white dark:bg-dark-800
        border border-dark-200 dark:border-dark-700
        rounded-xl shadow-sm
        overflow-hidden
        ${hover ? 'hover:shadow-md transition-shadow duration-200' : ''}
        ${className}
      `}
        >
            {children}
        </div>
    );
}

export function CardHeader({ children, className = '' }: CardHeaderProps) {
    return (
        <div
            className={`
        px-6 py-4
        border-b border-dark-200 dark:border-dark-700
        ${className}
      `}
        >
            {children}
        </div>
    );
}

export function CardBody({ children, className = '' }: CardBodyProps) {
    return (
        <div className={`px-6 py-4 ${className}`}>
            {children}
        </div>
    );
}

export function CardFooter({ children, className = '' }: CardFooterProps) {
    return (
        <div
            className={`
        px-6 py-4
        border-t border-dark-200 dark:border-dark-700
        bg-dark-50 dark:bg-dark-900
        ${className}
      `}
        >
            {children}
        </div>
    );
}
