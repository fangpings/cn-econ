import { readFileSync, readdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { resolve } from 'node:path'

const root = fileURLToPath(new URL('../textbook', import.meta.url))
const files = readdirSync(root)
  .filter(file => file.endsWith('.md') && /^\d{2}[a-z]?-/.test(file) && file !== '11-housing.md')
  .sort()

console.log(`Checking ${files.length} canonical chapters in cn-econ...`)

let errors = 0
for (const file of files) {
  const content = readFileSync(resolve(root, file), 'utf8')
  if (!/^# \d{2}[a-z]?\s+/m.test(content)) {
    console.error(`Missing standard title '# XX ...' in ${file}`)
    errors++
  }
}

if (errors > 0) {
  console.error(`Check failed with ${errors} error(s).`)
  process.exit(1)
} else {
  console.log(`All ${files.length} chapters passed format check.`)
}
