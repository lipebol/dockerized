import { spawnSync } from 'child_process'

export const cryptHandler = (encrypted) => {
    const mode = encrypted.endsWith('.jwe') ?
        `clevis-decrypt-tang < ./.dbsecrets/${encrypted}` :
        `echo "${encrypted}" | clevis-decrypt-tang`
    return spawnSync(mode, { shell: true, encoding: 'utf8' }).stdout.trim()
}