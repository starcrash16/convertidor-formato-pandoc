-- Archivo: archivos/section_break.lua

function RawBlock(el)
  -- Detecta el comando \newpage si Pandoc lo lee como LaTeX nativo
  if el.format == "tex" and el.text:match("\\newpage") then
    -- Inserta el XML raw de Word para un Salto de Sección (Página Siguiente)
    return pandoc.RawBlock('openxml', '<w:p><w:pPr><w:sectPr><w:type w:val="nextPage"/></w:sectPr></w:pPr></w:p>')
  end
end

function Para(el)
  -- Detecta \newpage si Pandoc lo lee como un párrafo de texto simple
  if #el.content == 1 and el.content[1].text == "\\newpage" then
    return pandoc.RawBlock('openxml', '<w:p><w:pPr><w:sectPr><w:type w:val="nextPage"/></w:sectPr></w:pPr></w:p>')
  end
end
