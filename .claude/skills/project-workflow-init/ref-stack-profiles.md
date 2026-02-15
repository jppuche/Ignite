# Stack Profiles Reference

Reference for adapting templates to detected project stack. Used in Step 2.1 to resolve domain-specific placeholders.

---

## Profile Selection Logic

Match the detected stack from Step 1.1 to the most specific profile. Priority:

1. If `pyproject.toml` with `[tool.django]` or `django` in dependencies → **Python (Django)**
2. If `pyproject.toml` with `fastapi` in dependencies → **Python (FastAPI)**
3. If `pyproject.toml` or `setup.py` or `setup.cfg` → **Python (generic)**
4. If `Cargo.toml` → **Rust**
5. If `go.mod` → **Go**
6. If `package.json` with `react`/`next`/`vue`/`svelte` in dependencies → **Node/React** (or equivalent framework)
7. If `package.json` with `express`/`fastify`/`hono`/`koa` → **Node/Express** (or equivalent)
8. If `package.json` (no framework detected) → **Node (generic)**
9. If `pom.xml` or `build.gradle` or `build.gradle.kts` → **Java/Kotlin**
10. If `composer.json` with `laravel` → **PHP (Laravel)**
11. If `composer.json` → **PHP (generic)**
12. If `Gemfile` with `rails` → **Ruby (Rails)**
13. If `Gemfile` → **Ruby (generic)**
14. Else → **Generic**

For full-stack projects (backend + frontend detected): apply backend profile for `{{DOMAIN_BACKEND}}` and frontend profile for `{{DOMAIN_FRONTEND}}`. Use the more specific framework to determine testing and styling.

### Package Manager Resolution (Node profiles only)

Detect lock file in project root:

| Lock file | `{{PACKAGE_MANAGER}}` | `{{PACKAGE_MANAGER_INSTALL}}` |
|-----------|----------------------|-------------------------------|
| `yarn.lock` | `yarn` | `yarn install --frozen-lockfile` |
| `pnpm-lock.yaml` | `pnpm` | `pnpm install --frozen-lockfile` |
| `bun.lockb` | `bun` | `bun install --frozen-lockfile` |
| `package-lock.json` or none | `npm` | `npm ci` |

Used in CI_SETUP `cache:` and install commands. Non-Node profiles ignore this.

---

## Quick Reference Table

| Profile | Backend Paths | Frontend Paths | Test Patterns | Styling | CI Setup Action |
|---------|--------------|----------------|---------------|---------|-----------------|
| Python (Django) | app/, views/, models/, urls/ | templates/, static/ | tests/, test_*.py | Conditional | setup-python@v5 |
| Python (FastAPI) | app/, routers/, models/, schemas/ | — | tests/, test_*.py | No | setup-python@v5 |
| Python (generic) | src/, lib/ | — | tests/, test_*.py | No | setup-python@v5 |
| Rust | src/, lib.rs, main.rs | — | tests/, #[cfg(test)] mod | No | rust-toolchain@stable |
| Go | cmd/, pkg/, internal/ | — | *_test.go (colocated) | No | setup-go@v5 |
| Node/React | src/lib/, src/app/api/, src/types/ | src/components/, src/app/, styles/ | __tests__/, *.test.ts(x) | Yes | setup-node@v4 |
| Node/Express | src/, routes/, middleware/, models/ | — | __tests__/, *.test.ts | No | setup-node@v4 |
| Node (generic) | src/, lib/ | — | __tests__/, *.test.ts | No | setup-node@v4 |
| Java/Kotlin | src/main/java/, src/main/kotlin/ | — | src/test/java/, src/test/kotlin/ | No | setup-java@v4 |
| PHP (Laravel) | app/, routes/, database/ | resources/views/, resources/js/ | tests/ | Conditional | setup-php@v2 |
| Ruby (Rails) | app/models/, app/controllers/ | app/views/, app/assets/ | spec/, test/ | Conditional | setup-ruby@v1 |
| Generic | src/, lib/ | — | tests/, test/ | No | (manual config) |

---

## Expanded Profiles

### Python (Django)

**Detection:** `pyproject.toml` or `requirements.txt` with `django` dependency.

**{{DOMAIN_BACKEND}}:**
```markdown
- app/ (o nombre de la app Django) -- modelos, vistas, URLs, forms
- manage.py -- punto de entrada Django
- settings/ o settings.py -- configuracion
- urls.py -- routing principal
- middleware/ -- middleware custom (si existe)
```

**{{DOMAIN_FRONTEND}}:**
```markdown
- templates/ -- templates HTML (Django template engine)
- static/ -- CSS, JS, imagenes
```

**{{TEST_DOMAIN}}:**
```markdown
- tests/ -- tests unitarios e integracion
- test_*.py, *_test.py -- tests por convencion pytest/unittest
- conftest.py -- fixtures compartidas
- Archivos de config de testing (pytest.ini, pyproject.toml [tool.pytest], setup.cfg)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "tests/**"
  - "**/test_*.py"
  - "**/*_test.py"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Sanitizacion de inputs (XSS via template escaping, SQL injection via ORM)
- CSRF protection en formularios ({% csrf_token %})
- Auth via Django auth framework (nunca custom crypto)
- Migraciones: siempre generar con makemigrations, nunca editar manualmente
```

**{{CRITICAL_RULES_FRONTEND}}:**
```markdown
- Templates Django: usar {{ variable|escape }} para contenido dinamico
- Static files: usar {% static %} tag, nunca paths absolutos
- Responsive: mobile-first, verificar en multiples breakpoints
```

**Styling Applicable:** Solo si hay `templates/` y `static/` con archivos CSS/JS.

**{{CI_SETUP}}:**
```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt || pip install -e .
```

---

### Python (FastAPI)

**Detection:** `pyproject.toml` or `requirements.txt` with `fastapi` dependency.

**{{DOMAIN_BACKEND}}:**
```markdown
- app/ -- aplicacion principal, punto de entrada
- routers/ -- endpoints por dominio (users, items, etc.)
- models/ -- modelos SQLAlchemy/Pydantic
- schemas/ -- schemas de validacion (request/response)
- services/ -- logica de negocio
- db/ -- conexion, migraciones (Alembic)
```

**{{DOMAIN_FRONTEND}}:** N/A (FastAPI es API-only por defecto).

**{{TEST_DOMAIN}}:**
```markdown
- tests/ -- tests unitarios e integracion
- test_*.py, *_test.py -- tests por convencion pytest
- conftest.py -- fixtures, TestClient setup
- Archivos de config de testing (pytest.ini, pyproject.toml [tool.pytest])
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "tests/**"
  - "**/test_*.py"
  - "**/*_test.py"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Validacion de inputs via Pydantic schemas (nunca manual)
- Dependency injection para DB sessions y auth
- Rate limiting en endpoints publicos (slowapi o middleware)
- Auth: OAuth2/JWT via fastapi.security, nunca custom crypto
```

**Styling Applicable:** No.

**{{CI_SETUP}}:**
```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt || pip install -e .
```

---

### Python (generic)

**Detection:** `pyproject.toml`, `setup.py`, or `setup.cfg` without Django/FastAPI.

**{{DOMAIN_BACKEND}}:**
```markdown
- src/ o nombre del paquete -- codigo fuente principal
- lib/ -- utilidades y logica compartida (si existe)
- scripts/ -- scripts auxiliares (si existe)
```

**{{DOMAIN_FRONTEND}}:** N/A.

**{{TEST_DOMAIN}}:**
```markdown
- tests/ -- tests unitarios e integracion
- test_*.py, *_test.py -- tests por convencion pytest
- conftest.py -- fixtures compartidas
- Archivos de config (pytest.ini, pyproject.toml [tool.pytest], tox.ini)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "tests/**"
  - "**/test_*.py"
  - "**/*_test.py"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Sanitizacion de inputs en boundaries (CLI args, file reads, network)
- Type hints en funciones publicas
- Manejo explicito de excepciones (no bare except)
```

**Styling Applicable:** No.

**{{CI_SETUP}}:**
```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -r requirements.txt || pip install -e .
```

---

### Rust

**Detection:** `Cargo.toml` present.

**{{DOMAIN_BACKEND}}:**
```markdown
- src/ -- codigo fuente (main.rs, lib.rs, modulos)
- benches/ -- benchmarks (si existe)
- examples/ -- codigo de ejemplo (si existe)
```

**{{DOMAIN_FRONTEND}}:** N/A.

**{{TEST_DOMAIN}}:**
```markdown
- tests/ -- tests de integracion
- src/**/mod.rs (#[cfg(test)] mod tests) -- tests unitarios colocados
- Archivos de config (Cargo.toml [profile.test])
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "tests/**"
  - "src/**/*.rs"
  - "benches/**"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Evitar unsafe excepto cuando sea estrictamente necesario (documentar razon)
- Error handling: usar Result<T, E> con thiserror/anyhow, no panic en librerias
- Ownership: preferir borrowing sobre cloning
- No unwrap() en codigo de produccion (usar ? o expect con mensaje)
```

**Styling Applicable:** No.

**{{CI_SETUP}}:**
```yaml
      - uses: dtolnay/rust-toolchain@stable
```

---

### Go

**Detection:** `go.mod` present.

**{{DOMAIN_BACKEND}}:**
```markdown
- cmd/ -- puntos de entrada (main packages)
- pkg/ -- librerias exportables
- internal/ -- codigo interno (no exportable)
- api/ -- definiciones de API (OpenAPI, protobuf)
```

**{{DOMAIN_FRONTEND}}:** N/A.

**{{TEST_DOMAIN}}:**
```markdown
- *_test.go -- tests colocados junto al codigo que testean
- testdata/ -- fixtures y datos de prueba
- Archivo de config (go.mod)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "**/*_test.go"
  - "**/testdata/**"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Error handling explicito (if err != nil), nunca ignorar errores
- Context propagation en funciones que tocan I/O o red
- Interfaces pequenas (1-3 metodos), definidas por el consumidor
- No goroutine leaks: siempre cancelar contexts, cerrar channels
```

**Styling Applicable:** No.

**{{CI_SETUP}}:**
```yaml
      - uses: actions/setup-go@v5
        with:
          go-version: 'stable'
```

---

### Node/React

**Detection:** `package.json` with `react`, `next`, `vue`, `svelte`, `angular` in dependencies.

**{{DOMAIN_BACKEND}}:**
```markdown
- src/lib/ -- logica de negocio, utilidades
- src/app/api/ -- endpoints API (Next.js route handlers)
- src/lib/db/ -- schema, conexion, migraciones
- src/types/ -- tipos compartidos
```

**{{DOMAIN_FRONTEND}}:**
```markdown
- src/components/ -- componentes reutilizables
- src/app/ -- paginas y layouts
- styles/ -- estilos globales
- public/ -- assets estaticos
```

**{{TEST_DOMAIN}}:**
```markdown
- __tests__/ -- tests unitarios e integracion
- *.test.ts, *.test.tsx -- tests colocados
- *.spec.ts -- tests E2E
- Archivos de config de testing (vitest.config.*, jest.config.*, playwright.config.*)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "**/*.test.*"
  - "**/*.spec.*"
  - "__tests__/**"
```

**{{STYLING_PATHS_FRONTMATTER}}:**
```yaml
  - "src/components/**"
  - "src/app/**"
  - "styles/**"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Sanitizacion de inputs (XSS, SQL injection)
- Rate limiting en endpoints publicos
- Auth server-side (nunca confiar en el cliente)
```

**{{CRITICAL_RULES_FRONTEND}}:**
```markdown
- Mobile-first responsive
- Dark mode en TODOS los componentes (usar CSS variables)
- Touch targets: 44x44px minimo
- Contraste: 4.5:1 minimo (WCAG AA)
- Skeleton loaders para estados de carga
- Estados vacios claros con CTA
```

**Styling Applicable:** Yes.

**{{CI_SETUP}}:**
```yaml
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: '{{PACKAGE_MANAGER}}'
      - run: {{PACKAGE_MANAGER_INSTALL}}
```

---

### Node/Express

**Detection:** `package.json` with `express`, `fastify`, `hono`, `koa` in dependencies (without frontend framework).

**{{DOMAIN_BACKEND}}:**
```markdown
- src/ -- codigo fuente principal
- routes/ -- definiciones de rutas/endpoints
- middleware/ -- middleware custom
- models/ -- modelos de datos
- services/ -- logica de negocio
```

**{{DOMAIN_FRONTEND}}:** N/A (API-only).

**{{TEST_DOMAIN}}:**
```markdown
- __tests__/ -- tests unitarios e integracion
- *.test.ts, *.spec.ts -- tests colocados
- Archivos de config de testing (vitest.config.*, jest.config.*)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "**/*.test.*"
  - "**/*.spec.*"
  - "__tests__/**"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Sanitizacion de inputs (XSS, SQL injection, NoSQL injection)
- Rate limiting en endpoints publicos
- Helmet.js para headers de seguridad
- Auth: JWT/session validacion en middleware, nunca en routes
```

**Styling Applicable:** No.

**{{CI_SETUP}}:**
```yaml
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: '{{PACKAGE_MANAGER}}'
      - run: {{PACKAGE_MANAGER_INSTALL}}
```

---

### Node (generic)

**Detection:** `package.json` without recognized framework.

**{{DOMAIN_BACKEND}}:**
```markdown
- src/ -- codigo fuente principal
- lib/ -- utilidades y logica compartida
```

**{{DOMAIN_FRONTEND}}:** N/A.

**{{TEST_DOMAIN}}:**
```markdown
- __tests__/ -- tests unitarios e integracion
- *.test.ts, *.test.js -- tests colocados
- Archivos de config de testing (vitest.config.*, jest.config.*)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "**/*.test.*"
  - "**/*.spec.*"
  - "__tests__/**"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Sanitizacion de inputs en boundaries
- Error handling: try/catch con tipos de error especificos
- No dependencias sin auditar (npm audit)
```

**Styling Applicable:** No.

**{{CI_SETUP}}:**
```yaml
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: '{{PACKAGE_MANAGER}}'
      - run: {{PACKAGE_MANAGER_INSTALL}}
```

---

### Java/Kotlin

**Detection:** `pom.xml`, `build.gradle`, or `build.gradle.kts` present.

**{{DOMAIN_BACKEND}}:**
```markdown
- src/main/java/ o src/main/kotlin/ -- codigo fuente
- src/main/resources/ -- configuracion, templates
```

**{{DOMAIN_FRONTEND}}:** N/A.

**{{TEST_DOMAIN}}:**
```markdown
- src/test/java/ o src/test/kotlin/ -- tests unitarios e integracion
- Archivos de config (pom.xml, build.gradle, application-test.properties)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "src/test/**"
  - "**/*Test.java"
  - "**/*Test.kt"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Sanitizacion de inputs (SQL injection via PreparedStatement/JPA)
- Manejo de excepciones: no catch generico, usar tipos especificos
- Thread safety: documentar clases no thread-safe
- Dependency injection via framework (Spring/Dagger), no instanciacion manual
```

**Styling Applicable:** No.

**{{CI_SETUP}}:**
```yaml
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '21'
      - run: ./gradlew build || mvn install -DskipTests
```

---

### PHP (Laravel)

**Detection:** `composer.json` with `laravel/framework` dependency.

**{{DOMAIN_BACKEND}}:**
```markdown
- app/ -- modelos, controladores, middleware, servicios
- routes/ -- definiciones de rutas (web.php, api.php)
- database/ -- migraciones, seeders, factories
- config/ -- configuracion de la aplicacion
```

**{{DOMAIN_FRONTEND}}:**
```markdown
- resources/views/ -- templates Blade
- resources/js/ -- JavaScript/Vue/React (si existe)
- resources/css/ -- estilos
- public/ -- assets compilados
```

**{{TEST_DOMAIN}}:**
```markdown
- tests/ -- tests unitarios (Unit/) e integracion (Feature/)
- Archivos de config (phpunit.xml)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "tests/**"
  - "**/*Test.php"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Validacion via Form Requests (nunca en controladores directamente)
- Eloquent: usar mass assignment protection ($fillable/$guarded)
- Auth via Laravel Guards/Policies, nunca custom
- CSRF protection automatica (verificar en API routes)
```

**{{CRITICAL_RULES_FRONTEND}}:**
```markdown
- Blade: usar {{ $variable }} para escape automatico, {!! !!} solo cuando sea seguro
- Assets: compilar via Vite/Mix, nunca incluir directamente
```

**Styling Applicable:** Solo si hay `resources/js/` o `resources/css/` con contenido.

**{{CI_SETUP}}:**
```yaml
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
      - run: composer install --no-interaction --prefer-dist
```

---

### Ruby (Rails)

**Detection:** `Gemfile` with `rails` gem.

**{{DOMAIN_BACKEND}}:**
```markdown
- app/models/ -- modelos ActiveRecord
- app/controllers/ -- controladores
- app/services/ -- objetos de servicio (si existe)
- config/ -- configuracion, rutas
- db/ -- migraciones, schema
```

**{{DOMAIN_FRONTEND}}:**
```markdown
- app/views/ -- templates ERB/Haml
- app/assets/ -- CSS, JS, imagenes
- app/javascript/ -- Stimulus/Turbo (si existe)
```

**{{TEST_DOMAIN}}:**
```markdown
- spec/ -- tests RSpec (si usa RSpec)
- test/ -- tests Minitest (si usa Minitest)
- Archivos de config (.rspec, Rakefile, rails_helper.rb)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "spec/**"
  - "test/**"
  - "**/*_spec.rb"
  - "**/*_test.rb"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Strong parameters en controladores (nunca params.permit!)
- Validaciones en modelos, no en controladores
- N+1 queries: usar includes/eager_load
- Auth via Devise/has_secure_password, nunca custom crypto
```

**{{CRITICAL_RULES_FRONTEND}}:**
```markdown
- ERB: usar <%= sanitize(content) %> para contenido dinamico inseguro
- Assets pipeline: usar helpers (image_tag, stylesheet_link_tag)
- Turbo/Stimulus: preferir sobre JavaScript vanilla
```

**Styling Applicable:** Solo si hay `app/views/` o `app/assets/` con contenido frontend.

**{{CI_SETUP}}:**
```yaml
      - uses: ruby/setup-ruby@v1
        with:
          bundler-cache: true
      - run: bundle install
```

---

### Generic

**Detection:** Fallback when no recognized config file is found.

**{{DOMAIN_BACKEND}}:**
```markdown
- src/ -- codigo fuente principal
- lib/ -- utilidades y logica compartida
```

**{{DOMAIN_FRONTEND}}:** N/A.

**{{TEST_DOMAIN}}:**
```markdown
- tests/ o test/ -- tests unitarios e integracion
- Archivos de config (inferir del stack)
```

**{{TEST_PATHS_FRONTMATTER}}:**
```yaml
  - "tests/**"
  - "test/**"
```

**{{CRITICAL_RULES_BACKEND}}:**
```markdown
- Sanitizacion de inputs en boundaries del sistema
- Error handling explicito (no silenciar errores)
- Documentar funciones publicas
```

**Styling Applicable:** No.

**{{CI_SETUP}}:**
```yaml
      # TODO: Configure CI setup steps for your stack
      - run: echo "Configure CI setup in .github/workflows/quality.yml"
```
