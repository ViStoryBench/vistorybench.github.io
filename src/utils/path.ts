export function getAssetBase(pathname: string): string {
  if (!pathname || pathname === '/') {
    return '.';
  }

  const segments = pathname.split('/').filter(Boolean);
  if (segments.length === 0) {
    return '.';
  }

  return segments.map(() => '..').join('/');
}

export function buildAssetPath(assetBase: string | undefined, target: string): string {
  const normalizedBase = (assetBase && assetBase.length > 0 ? assetBase : '.').replace(/\/$/, '');
  const sanitizedTarget = target.replace(/^\.\//, '').replace(/^\//, '');

  if (sanitizedTarget.length === 0) {
    return normalizedBase === '.' ? '.' : normalizedBase;
  }

  if (normalizedBase === '.') {
    return `./${sanitizedTarget}`.replace(/\/{2,}/g, '/');
  }

  return `${normalizedBase}/${sanitizedTarget}`.replace(/\/{2,}/g, '/');
}
