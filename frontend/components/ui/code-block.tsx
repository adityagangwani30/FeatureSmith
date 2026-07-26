"use client"

import React, { useState } from "react"
import { Check, Copy } from "lucide-react"
import { cn } from "@/lib/utils"

// ─── Tokenizer ───────────────────────────────────────────────────────────────

type TokenType =
  | "comment"
  | "string"
  | "keyword"
  | "number"
  | "function"
  | "operator"
  | "prompt"
  | "flag"
  | "success"
  | "error"
  | "plain"

interface Token {
  text: string
  type: TokenType
}

const PYTHON_KEYWORDS = new Set([
  "False", "None", "True", "and", "as", "assert", "async", "await",
  "break", "class", "continue", "def", "del", "elif", "else", "except",
  "finally", "for", "from", "global", "if", "import", "in", "is",
  "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
  "while", "with", "yield", "print",
])

function tokenizePythonLine(line: string): Token[] {
  const tokens: Token[] = []
  let i = 0

  while (i < line.length) {
    // Comment
    if (line[i] === "#") {
      tokens.push({ text: line.slice(i), type: "comment" })
      break
    }

    // String
    if (line[i] === '"' || line[i] === "'") {
      const q = line[i]
      // Check for triple quotes
      if (line.slice(i, i + 3) === q.repeat(3)) {
        const end = line.indexOf(q.repeat(3), i + 3)
        const j = end === -1 ? line.length : end + 3
        tokens.push({ text: line.slice(i, j), type: "string" })
        i = j
      } else {
        let j = i + 1
        while (j < line.length && line[j] !== q) {
          if (line[j] === "\\") j++
          j++
        }
        tokens.push({ text: line.slice(i, j + 1), type: "string" })
        i = j + 1
      }
      continue
    }

    // Number
    if (/[0-9]/.test(line[i])) {
      let j = i
      while (j < line.length && /[0-9._]/.test(line[j])) j++
      tokens.push({ text: line.slice(i, j), type: "number" })
      i = j
      continue
    }

    // r"..." raw string prefix
    if ((line[i] === "r" || line[i] === "f" || line[i] === "b") && (line[i + 1] === '"' || line[i + 1] === "'")) {
      const q = line[i + 1]
      let j = i + 2
      while (j < line.length && line[j] !== q) {
        if (line[j] === "\\") j++
        j++
      }
      tokens.push({ text: line.slice(i, j + 1), type: "string" })
      i = j + 1
      continue
    }

    // Identifier
    if (/[a-zA-Z_]/.test(line[i])) {
      let j = i
      while (j < line.length && /[a-zA-Z0-9_]/.test(line[j])) j++
      const word = line.slice(i, j)
      const isFn = line[j] === "("
      const type: TokenType = PYTHON_KEYWORDS.has(word) ? "keyword" : isFn ? "function" : "plain"
      tokens.push({ text: word, type })
      i = j
      continue
    }

    // Operator chars
    if (/[=<>!+\-*/%|&^~@]/.test(line[i])) {
      tokens.push({ text: line[i], type: "operator" })
      i++
      continue
    }

    // Fallthrough
    tokens.push({ text: line[i], type: "plain" })
    i++
  }

  return tokens
}

function tokenizeBashLine(line: string): Token[] {
  // Empty line
  if (!line.trim()) return [{ text: line, type: "plain" }]

  // Comment (not inside a command line)
  const trimmed = line.trimStart()
  if (trimmed.startsWith("#")) {
    const indent = line.slice(0, line.length - trimmed.length)
    return [
      ...(indent ? [{ text: indent, type: "plain" as TokenType }] : []),
      { text: trimmed, type: "comment" },
    ]
  }

  // Success indicator
  if (line.includes("✓")) return [{ text: line, type: "success" }]
  // Error indicator
  if (line.includes("✗")) return [{ text: line, type: "error" }]

  // Prompt line
  if (trimmed.startsWith("$")) {
    const indent = line.slice(0, line.length - trimmed.length)
    const rest = trimmed.slice(2) // strip "$ "
    const parts = rest.split(" ")
    const tokens: Token[] = []
    if (indent) tokens.push({ text: indent, type: "plain" })
    tokens.push({ text: "$ ", type: "prompt" })
    parts.forEach((part, idx) => {
      if (idx === 0) {
        tokens.push({ text: part, type: "function" })
      } else if (part.startsWith("--") || part.startsWith("-")) {
        tokens.push({ text: part, type: "flag" })
      } else if (part.startsWith('"') || part.startsWith("'")) {
        tokens.push({ text: part, type: "string" })
      } else {
        tokens.push({ text: part, type: "plain" })
      }
      if (idx < parts.length - 1) tokens.push({ text: " ", type: "plain" })
    })
    return tokens
  }

  return [{ text: line, type: "plain" }]
}

// ─── Token Renderer ──────────────────────────────────────────────────────────

const tokenClass: Record<TokenType, string> = {
  comment: "text-zinc-500 italic",
  string: "text-emerald-400",
  keyword: "text-blue-400",
  number: "text-orange-400",
  function: "text-yellow-300",
  operator: "text-zinc-400",
  prompt: "text-zinc-500 select-none",
  flag: "text-orange-300",
  success: "text-emerald-400",
  error: "text-red-400",
  plain: "text-zinc-200",
}

function renderTokens(tokens: Token[]): React.ReactNode {
  return tokens.map((tok, i) => (
    <span key={i} className={tokenClass[tok.type]}>
      {tok.text}
    </span>
  ))
}

// ─── Component ───────────────────────────────────────────────────────────────

interface CodeBlockProps {
  code: string
  language?: "python" | "bash" | "yaml"
  filename?: string
  showCopy?: boolean
  className?: string
}

export function CodeBlock({
  code,
  language = "python",
  filename,
  showCopy = true,
  className,
}: CodeBlockProps) {
  const [copied, setCopied] = useState(false)

  const lines = code.split("\n")

  const tokenize = (line: string): Token[] => {
    if (language === "bash") return tokenizeBashLine(line)
    return tokenizePythonLine(line)
  }

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div
      className={cn(
        "group relative overflow-hidden rounded-lg border border-zinc-800 bg-zinc-950",
        className
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 bg-zinc-900/80 px-4 py-2.5">
        <div className="flex items-center gap-3">
          {/* Traffic lights */}
          <div className="flex gap-1.5">
            <span className="h-3 w-3 rounded-full bg-zinc-700" />
            <span className="h-3 w-3 rounded-full bg-zinc-700" />
            <span className="h-3 w-3 rounded-full bg-zinc-700" />
          </div>
          {filename && (
            <span className="font-mono text-xs text-zinc-500">{filename}</span>
          )}
        </div>
        <div className="flex items-center gap-3">
          <span className="rounded bg-zinc-800 px-2 py-0.5 font-mono text-[10px] uppercase tracking-wide text-zinc-500">
            {language}
          </span>
          {showCopy && (
            <button
              onClick={handleCopy}
              aria-label="Copy code"
              className="rounded p-1 text-zinc-500 opacity-0 transition-all hover:bg-zinc-800 hover:text-zinc-300 group-hover:opacity-100"
            >
              {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
            </button>
          )}
        </div>
      </div>

      {/* Code area */}
      <pre className="overflow-x-auto p-5 text-[13px] leading-relaxed">
        <code>
          {lines.map((line, idx) => (
            <div key={idx} className="table-row">
              <span className="table-cell select-none pr-5 text-right font-mono text-zinc-700" aria-hidden>
                {idx + 1}
              </span>
              <span className="table-cell font-mono">{renderTokens(tokenize(line))}</span>
            </div>
          ))}
        </code>
      </pre>
    </div>
  )
}
