#-*- coding: utf-8 -*-
u"""

@author:		Martí Congost
@contact:		marti.congost@whads.com
@organization:	Whads/Accent SL
@since:			July 2008
"""
from cocktail.translations import translations
from cocktail.translations.helpers import ca_possessive, plural2, join
from cocktail.modeling import OrderedDict
from cocktail.stringutils import decapitalize
from cocktail import schema

translations.define("logged in as",
    ca = lambda user: u"Estàs identificat com a " \
            "<strong>%s</strong>" % translations(user, "ca"),
    es = lambda user: u"Estás identificado como " \
            "<strong>%s</strong>" % translations(user, "es"),
    en = lambda user: u"Logged in as "
            "<strong>%s</strong>" % translations(user, "en")
)

translations.define("Logout",
    ca = u"Sortir",
    es = u"Salir",
    en = u"Log out",
    fr = u"Log out",
    de = u"Abmelden",
    pl = u"Zaloguj się",
    nl = u"Log uit",
    pt = u"Sair"
)

translations.define("Type",
    ca = u"Tipus",
    es = u"Tipo",
    en = u"Type"
)

translations.define("woost.actions.new",
    ca = u"Nou",
    es = u"Nuevo",
    en = u"New"
)

translations.define("woost.actions.installation_sync",
    ca = u"Importar canvis",
    es = u"Importar cambios",
    en = u"Import changes"
)

translations.define("woost.actions.new.shortcut",
    ca = u"n",
    es = u"n",
    en = u"n"
)

translations.define("woost.actions.edit",
    ca = u"Fitxa",
    es = u"Ficha",
    en = u"Edit"
)

translations.define("woost.actions.edit.shortcut",
    ca = u"e",
    es = u"e",
    en = u"e"
)

translations.define("woost.actions.duplicate",
    ca = u"Duplicar",
    es = u"Duplicar",
    en = u"Duplicate"
)

translations.define("woost.actions.duplicate.shortcut",
    ca = u"u",
    es = u"u",
    en = u"u"
)

translations.define("woost.actions.order",
    ca = u"Ordenar",
    es = u"Ordenar",
    en = u"Order"
)

translations.define("woost.actions.move",
    ca = u"Moure",
    es = u"Mover",
    en = u"Move"
)

translations.define("woost.actions.delete",
    ca = u"Eliminar",
    es = u"Eliminar",
    en = u"Delete"
)

translations.define("woost.actions.delete.shortcut",
    ca = u"r",
    es = u"r",
    en = u"d"
)

translations.define("woost.actions.changelog",
    ca = u"Històric",
    es = u"Histórico",
    en = u"Changelog"
)

translations.define("woost.actions.add",
    ca = u"Afegir",
    es = u"Añadir",
    en = u"Add"
)

translations.define("woost.actions.add.shortcut",
    ca = u"a",
    es = u"a",
    en = u"a"
)

translations.define("woost.actions.add_integral",
    ca = u"Afegir",
    es = u"Añadir",
    en = u"Add"
)

translations.define("woost.actions.add_integral.shortcut",
    ca = u"a",
    es = u"a",
    en = u"a"
)

translations.define("woost.actions.remove",
    ca = u"Treure",
    es = u"Quitar",
    en = u"Remove"
)

translations.define("woost.actions.remove.shortcut",
    ca = u"r",
    es = u"r",
    en = u"r"
)

translations.define("woost.actions.diff",
    ca = u"Veure canvis",
    es = u"Ver cambios",
    en = u"Show changes"
)

translations.define("woost.actions.diff.shortcut",
    ca = u"c",
    es = u"c",
    en = u"c"
)

translations.define("woost.actions.preview",
    ca = u"Vista prèvia",
    es = u"Vista previa",
    en = u"Preview"
)

translations.define("woost.actions.preview.shortcut",
    ca = u"p",
    es = u"p",
    en = u"p"
)

translations.define("woost.actions.open_resource",
    ca = u"Veure publicat",
    es = u"Ver publicado",
    en = u"Show published"
)

translations.define("woost.actions.open_resource.shortcut",
    ca = u"b",
    es = u"b",
    en = u"b"
)

translations.define("woost.actions.references",
    ca = u"Referències",
    es = u"Referencias",
    en = u"References"
)

translations.define("woost.actions.references.shortcut",
    ca = u"f",
    es = u"f",
    en = u"f"
)

translations.define("woost.actions.upload_files",
    ca = u"Importar fitxers",
    es = u"Importar ficheros",
    en = u"Import files"
)

translations.define("woost.actions.export_xls",
    ca = u"Exportar a MS Excel",
    es = u"Exportar a MS Excel",
    en = u"Export to MS Excel"
)

translations.define("woost.actions.save",
    ca = u"Desar",
    es = u"Guardar",
    en = u"Save"
)

translations.define("woost.actions.save_and_close",
    ca = u"Desar i tancar",
    es = u"Guardar y cerrar",
    en = u"Save and close"
)

translations.define("woost.actions.save_and_close.shortcut",
    ca = u"s",
    es = u"g",
    en = u"s"
)

translations.define("woost.actions.invalidate_cache",
    ca = u"Netejar el cache",
    es = u"Limpiar el cache",
    en = u"Clear cache"
)

translations.define("woost.actions.select",
    ca = u"Seleccionar",
    es = u"Seleccionar",
    en = u"Select"
)

translations.define("woost.actions.select.shortcut",
    ca = u"s",
    es = u"s",
    en = u"s"
)

translations.define("woost.actions.close",
    ca = u"Tancar",
    es = u"Cerrar",
    en = u"Close"
)

translations.define("woost.actions.close.shortcut",
    ca = u"c",
    es = u"c",
    en = u"c"
)

translations.define("woost.actions.cancel",
    ca = u"Cancelar",
    es = u"Cancelar",
    en = u"Cancel"
)

translations.define("woost.actions.cancel.shortcut",
    ca = u"c",
    es = u"c",
    en = u"c"
)

translations.define("woost.actions.edit_blocks",
    ca = u"Editar blocs",
    es = u"Editar bloques",
    en = u"Edit blocks"
)

translations.define(
    "woost.controllers.backoffice.editstack.EditBlocksNode-instance",
    ca = lambda instance:
        u"Editant els blocs " + ca_possessive(translations(instance.item)),
    es = lambda instance:
        u"Editando los bloques de " + translations(instance.item),
    en = lambda instance:
        u"Editing the blocks for " + translations(instance.item)
)

translations.define("woost.views.BlockSection.edit_slot_link",
    ca = u"Editar aquest espai",
    es = u"Editar este espacio",
    en = u"Edit this slot"
)

translations.define("editing",
    ca = lambda item:
        u"Editant %s <em>'%s'</em>"
        % (translations(item.__class__.name, "ca").lower(),
           translations(item, "ca")),
    es = lambda item:
        u"Editando %s <em>'%s'</em>"
        % (translations(item.__class__.name, "es").lower(),
           translations(item, "es")),
    en = lambda item:
        u"Editing %s <em>'%s'</em>"
        % (translations(item.__class__.name, "es").lower(),
           translations(item, "es"))
)

translations.define("creating",
    ca = lambda content_type:
        u"Creant %s" % translations(content_type.__name__, "ca").lower(),
    es = lambda content_type:
        u"Creando %s" % translations(content_type.__name__, "es").lower(),
    en = lambda content_type:
        u"Creating new %s" % translations(content_type.__name__, "en").lower()
)

translations.define("woost.views.BackOfficeLayout edit stack select",
    ca = lambda type = None, relation = None:
        u"Seleccionar %s"
        % translations(relation if relation else type.name).lower(),
    es = lambda type = None, relation = None:
        u"Seleccionar %s"
        % translations(relation if relation else type.name).lower(),
    en = lambda type = None, relation = None:
        u"Select %s"
        % translations(relation if relation else type.name).lower()
)

translations.define("woost.views.BackOfficeLayout edit stack add",
    ca = lambda relation: u"Afegir %s" % translations(relation).lower(),
    es = lambda relation: u"Añadir %s" % translations(relation).lower(),
    en = lambda relation: u"Add %s" % translations(relation).lower()
)

translations.define("Backout",
    ca = u"Desfer",
    es = u"Deshacer",
    en = u"Backout"
)

translations.define("woost.views.BackOfficeShowDetailView revert",
    ca = u"Desfer",
    es = u"Deshacer",
    en = u"Undo"
)

translations.define("Discard changes",
    ca = u"Descartar",
    es = u"Descartar",
    en = u"Discard"
)

translations.define("Forget",
    ca = u"Oblidar",
    es = u"Olvidar",
    en = u"Forget"
)

translations.define("woost.views.ContentTable sort ascending",
    ca = u"Ordre ascendent",
    es = u"Orden ascendente",
    en = u"Ascending order"
)

translations.define("woost.views.ContentTable sort descending",
    ca = u"Ordre descendent",
    es = u"Orden descendente",
    en = u"Descending order"
)

translations.define("woost.views.ContentTable add column filter",
    ca = u"Afegir un filtre",
    es = u"Añadir un filtro",
    en = u"Add a filter"
)

translations.define("BackOfficeContentView.tree",
    ca = u"Estructura",
    es = u"Estructura",
    en = u"Tree"
)

translations.define("BackOfficeContentView.element",
    ca = u"Descripció de l'objecte",
    es = u"Descripción del objeto",
    en = u"Object description"
)

translations.define("BackOfficeContentView.thumbnail",
    ca = u"Miniatura",
    es = u"Miniatura",
    en = u"Thumbnail"
)

translations.define("woost.views.ContentView.content_type_selector.shortcut",
    ca = u"t",
    es = u"t",
    en = u"t"
)

translations.define("woost.views.ContentView.content_view_dropdown.shortcut",
    ca = u"v",
    es = u"v",
    en = u"v"
)

translations.define("woost.views.BackOfficeContentView add user view",
    ca = u"Crear vista",
    es = u"Crear vista",
    en = u"New view"
)

translations.define("ContentView search",
    ca = u"Cercar",
    es = u"Buscar",
    en = u"Search"
)

translations.define("woost.views.ContentView show advanced search",
    ca = u"Més opcions de cerca",
    es = u"Mas opciones de búsqueda",
    en = u"More search options"
)

translations.define("woost.views.ContentView close advanced search",
    ca = u"Descartar la cerca",
    es = u"Descartar la búsqueda",
    en = u"Discard search"
)

translations.define("woost.views.ContentView search button",
    ca = u"Cercar",
    es = u"Buscar",
    en = u"Search"
)

translations.define("Advanced search",
    ca = u"Cerca avançada",
    es = u"Búsqueda avanzada",
    en = u"Advanced search"
)

translations.define("woost.views.TreeContentView expansion controls",
    ca = u"Arbre:",
    es = u"Árbol:",
    en = u"Tree:"
)

translations.define("woost.views.TreeContentView expand all",
    ca = u"Desplegar",
    es = u"Expandir",
    en = u"Unfold"
)

translations.define("woost.views.TreeContentView collapse all",
    ca = u"Plegar",
    es = u"Contraer",
    en = u"Fold"
)

translations.define("Differences for",
    ca = lambda item: u"Canvis a <em>'%s'</em>" % translations(item, "ca"),
    es = lambda item: u"Cambios en <em>'%s'</em>" % translations(item, "es"),
    en = lambda item: u"Changes in <em>'%s'</em>" % translations(item, "en")
)

translations.define("woost.views.ObjectDiff.no_differences",
    ca = u"L'element no té cap canvi.",
    es = u"El elemento no tiene ningún cambio.",
    en = u"The item has no changes."
)

translations.define("woost.actions.revert",
    ca = u"Desfer",
    es = u"Deshacer",
    en = u"Undo"
)

translations.define("woost.actions.add_block",
    ca = u"Afegir",
    es = u"Añadir",
    en = u"Add"
)

translations.define("woost.actions.add_block_before",
    ca = u"Afegir davant",
    es = u"Añadir en frente",
    en = u"Add before"
)

translations.define("woost.actions.add_block_after",
    ca = u"Afegir darrere",
    es = u"Añadir detrás",
    en = u"Add after"
)

translations.define("woost.actions.edit_block",
    ca = u"Editar",
    es = u"Editar",
    en = u"Edit"
)

translations.define("woost.actions.remove_block",
    ca = u"Treure",
    es = u"Quitar",
    en = u"Remove"
)

translations.define("woost.actions.copy_block",
    ca = u"Copiar",
    es = u"Copiar",
    en = u"Copy"
)

translations.define("woost.actions.cut_block",
    ca = u"Retallar",
    es = u"Cortar",
    en = u"Cut"
)

translations.define("woost.actions.paste_block",
    ca = u"Enganxar",
    es = u"Pegar",
    en = u"Paste"
)

translations.define("woost.actions.paste_block_after",
    ca = u"Enganxar darrere",
    es = u"Pegar detrás",
    en = u"Paste after"
)

translations.define("woost.actions.paste_block_before",
    ca = u"Enganxar davant",
    es = u"Pegar delante",
    en = u"Paste before"
)

translations.define("woost.actions.share_block",
    ca = u"Afegir a la llibreria",
    es = u"Añadir a la libreria",
    en = u"Add to the library"
)

translations.define("woost.views.ActionBar Additional actions",
    ca = u"Més accions",
    es = u"Más acciones",
    en = u"More actions"
)

translations.define("datetime format",
    ca = "%d/%m/%Y %H:%M",
    es = "%d/%m/%Y %H:%M",
    en = "%Y-%m-%d %H:%M"
)

translations.define("BackOfficeOrderView last position",
    ca = u"-- Final de la llista --",
    es = u"-- Final de la lista --",
    en = u"-- End of the list --"
)

translations.define("woost.views.BackOfficeOrderView.stack_node_description",
    ca = u"ordenar",
    es = u"ordenar",
    en = u"rearrange"
)

translations.define(
    "woost.views.BackOfficeOrderView.insertion_point_explanation",
    ca = u"Els elements seleccionats es situaran <em>davant</em> del punt "
        u"indicat:",
    es = u"Los elementos seleccionados se situarán <em>delate</em> del punto "
        u"indicado:",
    en = u"The selected items will be inserted <em>before</em> the specified "
        u"point:"
)

translations.define(
    "woost.controllers.backoffice.movecontroller.TreeCycleError-instance",
    ca = u"No es pot inserir un element dins de sí mateix.",
    es = u"No se puede insertar un elemento dentro de si mismo.",
    en = u"Can't insert an element into itself."
)

translations.define(
    "woost.controllers.backoffice.DragAndDropController.drop_notification",
    ca = lambda dragged_object, target_object, target_member:
        (
            u"S'ha establert %s com a %s %s"
            if isinstance(target_member, schema.Reference)
            else u"S'ha afegit %s a %s %s"
        ) % (
            translations(dragged_object),
            translations(target_member),
            ca_possessive(translations(target_object))
        ),
    es = lambda dragged_object, target_object, target_member:
        (
            u"Se ha establecido %s como %s de %s"
            if isinstance(target_member, schema.Reference)
            else u"Se ha añadido %s a %s de %s"
        ) % (
            translations(dragged_object),
            translations(target_member),
            translations(target_object)
        ),
    en = lambda dragged_object, target_object, target_member:
        (
            u"%s set as %s of %s"
            if isinstance(target_member, schema.Reference)
            else u"%s added to the %s of %s"
        ) % (
            translations(dragged_object),
            translations(target_member),
            translations(target_object)
        )
)

translations.define("woost.views.BackOfficeLayout.drop",
    ca = u"Inserir a dins",
    es = u"Insertar dentro",
    en = u"Insert inside"
)

translations.define("woost.views.BackOfficeLayout.drop_before",
    ca = u"Inserir davant",
    es = u"Insertar en frente",
    en = u"Insert before"
)

translations.define("woost.views.BackOfficeLayout.drop_after",
    ca = u"Inserir darrere",
    es = u"Insertar detrás",
    en = u"Insert after"
)

def _selection_error_ca(instance):
    if instance.action.min and instance.selection_size < instance.action.min:
        bound = instance.action.min
        bound_label = u"mínim"
    else:
        bound = instance.action.max
        bound_label = u"màxim"

    return (
        u"No es pot aplicar l'acció <em>%s</em> a una selecció %s; "
        u"el %s és %s" % (
            translations(instance.action).lower(),
            plural2(
                instance.selection_size,
                u"d'un sol element",
                u"de %d elements" % instance.selection_size
            ),
            bound_label,
            plural2(
                bound,
                u"d'un element",
                u"de %d elements" % bound
            )
        )
    )

def _selection_error_es(instance):
    if instance.action.min and instance.selection_size < instance.action.min:
        bound = instance.action.min
        bound_label = u"mínimo"
    else:
        bound = instance.action.max
        bound_label = u"máximo"

    return (
        u"No se puede aplicar la acción <em>%s</em> a una selección de %s; "
        u"el %s es de %s" % (
            translations(instance.action).lower(),
            plural2(
                instance.selection_size,
                u"de un solo elemento",
                u"%d elementos" % instance.selection_size
            ),
            bound_label,
            plural2(
                bound,
                u"un elemento",
                u"%d elementos" % bound
            )
        )
    )

def _selection_error_en(instance):
    if instance.action.min and instance.selection_size < instance.action.min:
        bound = instance.action.min
        bound_label = u"at least"
    else:
        bound = instance.action.max
        bound_label = u"no more than"

    return (
        u"Can't apply action <em>%s</em> to a selection consisting of %s; "
        u"must select %s %s" % (
            translations(instance.action).lower(),
            plural2(
                instance.selection_size,
                u"a single element",
                u"%d elements" % instance.selection_size
            ),
            bound_label,
            plural2(
                bound,
                u"one element",
                u"%d elements" % bound
            )
        )
    )

translations.define(
    "woost.controllers.backoffice.useractions.SelectionError-instance",
    ca = _selection_error_ca,
    es = _selection_error_es,
    en = _selection_error_en
)

translations.define(
    "woost.controllers.backoffice.editstack.WrongEditStackError-instance",
    ca = u"La sessió d'edició indicada no existeix o ha expirat.",
    es = u"La sesión de edición indicada no existe o ha expirado.",
    en = u"The indicated edit session doesn't exist, or has expired."
)


translations.define(
    "woost.controllers.backoffice.fileeditnode.FileRequiredError-instance",
    ca = u"S'ha de carregar un fitxer o seleccionar un fitxer local",
    es = u"Debe subirse un fichero o seleccionar un fichero local",
    en = u"Must upload a file, or select a local file"
)

translations.define(
    "forbidden value",
    ca = u"Camp restringit",
    es = u"Campo restringido",
    en = u"Restricted field"
)

translations.define("woost.views.BackOfficeDeleteView.warning",
    ca = u"S'eliminaran els elements indicats:",
    es = u"Se eliminarán los elementos indicados:",
    en = u"The following elements will be deleted:"
)

translations.define("woost.views.BackOfficeDeleteView.block_notice",
    ca = u"No es pot completar l'eliminació, ja que alguns dels elements  "
         u"seleccionats tenen contingut relacionat que impedeix que puguin "
         u"ser eliminats:",
    es = u"No se puede completar la eliminación, ya que algunos de los "
         u"elementos seleccionados contienen vinculaciones que impiden que "
         u"puedan ser eliminados:",
    en = u"The delete operation could not be executed; it is blocked by the "
         u"the following relations:"
)

translations.define("woost.views.BackOfficeDeleteView.cascade_details",
    ca = u"També eliminarà:",
    es = u"También eliminará:",
    en = u"Will also delete:"
)

translations.define("woost.views.BackOfficeDeleteView.block_details",
    ca = u"Bloquejat per:",
    es = u"Bloqueado por:",
    en = u"Blocked by:"
)

translations.define("woost.views.BackOfficeDeleteView.confirm_delete_button",
    ca = u"Eliminar",
    es = u"Eliminar",
    en = u"Delete"
)

translations.define("woost.views.BackOfficeDeleteView.cancel_button",
    ca = u"Cancel·lar",
    es = u"Cancelar",
    en = u"Cancel"
)

translations.define("woost.views.ItemSelector select",
    ca = u"Llistat",
    es = u"Listado",
    en = u"Listing"
)

translations.define("woost.views.ItemSelector new",
    ca = u"Nou",
    es = u"Nuevo",
    en = u"New"
)

translations.define("woost.views.ItemSelector edit",
    ca = u"Editar",
    es = u"Editar",
    en = u"Edit"
)

translations.define("woost.views.ItemSelector delete",
    ca = u"Eliminar",
    es = u"Eliminar",
    en = u"Delete"
)

translations.define("woost.views.BackOfficeItemSelectorView title",
    ca = lambda type: "Seleccionar " + translations(type.name, "ca").lower(),
    es = lambda type: "Seleccionar " + translations(type.name, "es").lower(),
    en = lambda type: "Select " + translations(type.name, "en").lower()
)

translations.define("woost.views.BackOfficeShowDetailView open resource",
    ca = u"Obrir el fitxer",
    es = u"Abrir el fichero",
    en = u"Show file"
)

translations.define(
    "woost.models.userfilter.IsPublishedFilter-instance",
    ca = u"Elements publicats",
    es = u"Elementos publicados",
    en = u"Published elements"
)

translations.define("woost.models.userfilter.TypeFilter-instance",
    ca = u"Tipus",
    es = u"Tipo",
    en = u"Type"
)

translations.define("UserFilter.is_inherited",
    ca = u"Inclou fills",
    es = u"Incluye hijos",
    en = u"Children included"
)

translations.define("woost.views.BackOfficeChangeLogView title",
    ca = u"Històric",
    es = u"Histórico",
    en = u"Changelog"
)

translations.define("woost.views.BackOfficeChangeLogView collapsed",
    ca = u"%(count)s canvis",
    es = u"%(count)s cambios",
    en = u"%(count)s changes"
)

translations.define("woost.views.BackOfficeChangeLogView expanded",
    ca = u"Tornar a ocultar",
    es = u"Volver a ocultar",
    en = u"Fold"
)

translations.define("woost.views.NotificationBox.close_notification_button",
    ca = u"Ocultar aquest missatge",
    es = u"Ocultar este mensaje",
    en = u"Hide this message"
)

translations.define("woost.controllers.notifications.Notification-instance",
    ca = lambda instance: instance.message,
    es = lambda instance: instance.message,
    en = lambda instance: instance.message
)

# woost.views.EditLink
#------------------------------------------------------------------------------
translations.define("woost.views.EditLink-publishable_target",
    ca = u"aquesta pàgina",
    es = u"esta página",
    en = u"this page"
)

translations.define("woost.views.EditLink-site",
    ca = u"les propietats del lloc web",
    es = u"las propiedades del sitio web",
    en = u"site-wide properties"
)

translations.define("woost.views.EditLink-create",
    ca = lambda target_desc = None:
        u"Crear " + (target_desc or u"element"),
    es = lambda target_desc = None:
        u"Crear " + (target_desc or u"elemento"),
    en = lambda target_desc = None:
        u"Create " + (target_desc or u"element")
)

translations.define("woost.views.EditLink-modify",
    ca = lambda target_desc = None:
        u"Editar " + (target_desc or u"això"),
    es = lambda target_desc = None:
        u"Editar " + (target_desc or u"esto"),
    en = lambda target_desc = None:
        u"Edit " + (target_desc or u"this")
)

translations.define("woost.views.EditLink-delete",
    ca = lambda target_desc = None:
        u"Eliminar " + (target_desc or u"això"),
    es = lambda target_desc = None:
        u"Eliminar " + (target_desc or u"esto"),
    en = lambda target_desc = None:
        u"Delete " + (target_desc or u"this")
)

# ItemDisplay
#------------------------------------------------------------------------------
translations.define("woost.views.ItemDisplay.toggle_button",
    ca = u"Mostrar detalls de l'element",
    es = u"Mostrar detalles del elemento",
    en = u"Show details for this item"
)

# Initialization content
#------------------------------------------------------------------------------
translations.define(
    "woost.initialization.website.site_name",
    ca = u"El meu lloc web",
    es = u"Mi sitio web",
    en = u"My website"
)

translations.define(
    "woost.initialization.anonymous.title",
    ca = u"Anònim",
    es = u"Anónimo",
    en = u"Anonymous"
)

translations.define(
    "woost.initialization.administrators.title",
    ca = u"Administradors",
    es = u"Administradores",
    en = u"Administrators"
)

translations.define(
    "woost.initialization.everybody.title",
    ca = u"Tothom",
    es = u"Todos los usuarios",
    en = u"Everybody"
)

translations.define(
    "woost.initialization.authenticated.title",
    ca = u"Autenticat",
    es = u"Autenticado",
    en = u"Authenticated"
)

translations.define(
    "woost.initialization.editors.title",
    ca = u"Editors",
    es = u"Editores",
    en = u"Editors"
)

translations.define("woost.initialization.file_deletion_trigger.title",
    ca = u"Esborrar fitxers del disc quan s'elimini el seu element",
    es = u"Borrar ficheros del disco cuando se elimine su elemento",
    en = u"Erase files from disc when their item is deleted"
)

translations.define("woost.initialization.document_controller.title",
    ca = u"Controlador de document",
    es = u"Controlador de documento",
    en = u"Document controller"
)

translations.define("woost.initialization.file_controller.title",
    ca = u"Controlador de fitxer",
    es = u"Controlador de fichero",
    en = u"File controller"
)

translations.define("woost.initialization.uri_controller.title",
    ca = u"Controlador de redirecció",
    es = u"Controlador de redirección",
    en = u"Redirection controller"
)

translations.define("woost.initialization.styles_controller.title",
    ca = u"Controlador d'estils d'usuari",
    es = u"Controlador de estilos de usuario",
    en = u"User styles controller"
)

translations.define("woost.initialization.feed_controller.title",
    ca = u"Controlador de sindicació de continguts",
    es = u"Controlador de sindicación de contenidos",
    en = u"Feed controller"
)

translations.define("woost.initialization.backoffice_controller.title",
    ca = u"Controlador de panell administratiu",
    es = u"Controlador de panel administrativo",
    en = u"Backoffice controller"
)

translations.define("woost.initialization.firstchildredirection_controller.title",
    ca = u"Controlador de redirecció automàtica al primer fill",
    es = u"Controlador de redirección automática al primer hijo",
    en = u"First child redirection controller"
)

translations.define("woost.initialization.login_controller.title",
    ca = u"Controlador de autenticació d'usuari",
    es = u"Controlador de autenticación de usuario",
    en = u"User authentication controller"
)

translations.define("woost.initialization.passwordchange_controller.title",
    ca = u"Controlador de canvi de contrasenya",
    es = u"Controlador de cambio de contraseña",
    en = u"Password change controller"
)

translations.define("woost.initialization.passwordchangeconfirmation_controller.title",
    ca = u"Controlador de confirmació de canvi de contrasenya",
    es = u"Controlador de confirmación de cambio de contraseña",
    en = u"Password change confirmation controller"
)

translations.define(
    "woost.initialization.standard_template.title",
    ca = u"Plantilla estàndard",
    es = u"Plantilla estándar",
    en = u"Standard template"
)

translations.define(
    "woost.initialization.home.title",
    ca = u"Lloc web",
    es = u"Sitio web",
    en = u"Web site"
)

translations.define(
    "woost.initialization.home.inner_title",
    ca = u"Benvingut!",
    es = u"Bienvenido!",
    en = u"Welcome!"
)

translations.define(
    "woost.initialization.home.body",
    ca = u"<p>El teu lloc web s'ha creat correctament. Ja pots començar "
        u"a <a href='/cms'>treballar-hi</a> i substituir aquesta pàgina "
        u"amb els teus propis continguts.</p>",
    es = u"<p>Tu sitio web se ha creado correctamente. Ya puedes empezar "
        u"a <a href='/cms'>trabajar</a> en él y sustituir esta página "
        u"con tus propios contenidos.</p>",
    en = u"<p>Your web site has been created successfully. You can start "
        u"<a href='/cms'>working on it</a> and replace this page with "
        u"your own content.</p>"
)

translations.define(
    "woost.initialization.user_styles.title",
    ca = u"Estils d'usuari",
    es = u"Estilos de usuario",
    en = u"User styles"
)

translations.define(
    "woost.initialization.backoffice.title",
    ca = u"Gestor de continguts",
    es = u"Gestor de contenidos",
    en = u"Content Manager"
)

translations.define(
    "woost.initialization.not_found_error_page.title",
    ca = u"Pàgina no trobada",
    es = u"Página no encontrada",
    en = u"Page not found"
)

translations.define(
    "woost.initialization.not_found_error_page.body",
    ca = u"<p>La direcció indicada no coincideix amb cap dels continguts "
         u"del web. Si us plau, revísa-la i torna-ho a provar.</p>",
    es = u"<p>La dirección indicada no coincide con ninguno de los "
         u"contenidos del web. Por favor, revísala y inténtalo de nuevo.</p>",
    en = u"<p>Couldn't find the indicated address. Please, verify it and try "
         u"again.</p>"
)

translations.define(
    "woost.initialization.forbidden_error_page.title",
    ca = u"Accés denegat",
    es = u"Acceso denegado",
    en = u"Forbidden",
    pt = u"Acesso negado"
)

translations.define(
    "woost.initialization.forbidden_error_page.body",
    ca = u"<p>No es permet l'accés a aquesta secció del web.</p>",
    es = u"<p>No se permite el acceso a esta sección del sitio.</p>",
    en = u"<p>Access denied.</p>",
    pt = u"<p>Não é permitido o acesso a esta seção do site.</p>"
)

translations.define(
    "woost.initialization.password_change_page.title",
    ca = u"Canvi de contrasenya d'usuari",
    es = u"Cambio de contraseña de usuario",
    en = u"Password change",
    pt = u"Alterar chave de acesso"
)

translations.define(
    "woost.initialization.password_change_page.body",
    ca = u"<p>Introdueix el teu identificador d'usuari per iniciar el "
         u"procés de canvi de contrasenya</p>",
    es = u"<p>Introduce a tu identificador de usuario para iniciar el "
         u"proceso de cambio de contraseña</p>",
    en = u"<p>Enter your user identifier below to start the password "
         u"change process</p>""",
    pt = u"""<p>Introduza o seu endereço eletrónico para iniciar o processo de
    alteração da palavra-passe. Enviar-lhe-emos um e-mail para o efeito.</p>"""
)

translations.define(
    "woost.initialization.password_change_page.form_title",
    ca = u"Formulari de petició de canvi de contrasenya",
    es = u"Formulario de petición de cambio de contraseña",
    en = u"Password change request form"
)

translations.define(
    "woost.initialization.password_change_confirmation_page.title",
    ca = u"Canvi de contrasenya",
    es = u"Cambio de contraseña",
    en = u"Change your password",
    pt = u"Alterar chave de acesso"
)

translations.define(
    "woost.initialization.password_change_confirmation_page.body",
    ca = u"<p>Introduïx la nova contrasenya pel teu compte d'usuari:</p>",
    es = u"<p>Introduce tu nueva contraseña para tu cuenta de usuario:</p>",
    en = u"<p>Enter the new password for your user account:</p>",
    pt = u"<p>Digite a nova senha para a sua conta de usuário:</p>"
)

translations.define(
    "woost.initialization.password_change_confirmation_page.form_title",
    ca = u"Formulari de canvi de contrasenya",
    es = u"Formulario de cambio de contraseña",
    en = u"Password change form"
)

translations.define(
    "woost.initialization.password_change_email_template.title",
    ca = u"Plantilla de correu electrònic per sol·licitar el canvi de contrasenya",
    es = u"Plantilla de correo electrónico para solicitud de cambio de contraseña",
    en = u"Password change confirmation email template"
)

translations.define(
    "woost.initialization.password_change_email_template.subject",
    ca = u"Canvi de contrasenya",
    es = u"Cambio de contraseña",
    en = u"Password change"
)

translations.define(
    "woost.initialization.password_change_email_template.body",
    ca = u"""Obre l'enllaç següent per establir la teva nova contrasenya:<br/>
        <a href='${confirmation_url}'>${confirmation_url}</a>""",
    es = u"""Abre el enlace siguiente para establecer tu nueva contraseña:<br/>
        <a href='${confirmation_url}'>${confirmation_url}</a>""",
    en = u"""Open the following link to set your new password:<br/>
        <a href='${confirmation_url}'> ${confirmation_url}</a>"""
)

translations.define(
    "woost.initialization.login_page.title",
    ca = u"Autenticació d'usuari",
    es = u"Autenticación de usuario",
    en = u"User authentication"
)

translations.define(
    "woost.initialization.own_items_user_view.title",
    ca = u"Els meus elements",
    es = u"Mis elementos",
    en = u"My items"
)

translations.define(
    "woost.initialization.page_tree_user_view.title",
    ca = u"Arbre de pàgines",
    es = u"Árbol de páginas",
    en = u"Page tree"
)

translations.define(
    "woost.initialization.file_gallery_user_view.title",
    ca = u"Galeria de fitxers",
    es = u"Galería de ficheros",
    en = u"File gallery"
)


translations.define("woost.initialization.content_renderer.title",
    ca = u"Imatge del contingut",
    es = u"Imagen del contenido",
    en = u"Content renderer"
)

translations.define("woost.initialization.icon16_renderer.title",
    ca = u"Icones de 16x16",
    es = u"Iconos de 16x16",
    en = u"16x16 icons"
)

translations.define("woost.initialization.icon32_renderer.title",
    ca = u"Icones de 32x32",
    es = u"Iconos de 32x32",
    en = u"32x32 icons"
)

translations.define("woost.initialization.default_image_factory.title",
    ca = u"Imatge sense processar",
    es = u"Imagen sin procesar",
    en = u"Unprocessed image"
)

translations.define("woost.initialization.icon16_image_factory.title",
    ca = u"Icona de 16x16",
    es = u"Icono de 16x16",
    en = u"16x16 icon"
)

translations.define("woost.initialization.icon32_image_factory.title",
    ca = u"Icona de 32x32",
    es = u"Icono de 32x32",
    en = u"32x32 icon"
)

translations.define(
    "woost.initialization.backoffice_thumbnail_image_factory.title",
    ca = u"Vista en miniatura del panell d'administració",
    es = u"Vista en miniatura del panel de administración",
    en = u"Backoffice thumbnail"
)

translations.define(
    "woost.initialization.backoffice_small_thumbnail_image_factory.title",
    ca = u"Vista en miniatura petita del panell d'administració",
    es = u"Vista en miniatura pequeña del panel de administración",
    en = u"Backoffice small thumbnail"
)

translations.define(
    "woost.initialization.edit_blocks_thumbnail_image_factory.title",
    ca = u"Vista en miniatura de l'editor de blocs",
    es = u"Vista en miniatura del editor de bloques",
    en = u"Block editor thumbnail"
)

translations.define(
    "woost.initialization.close_up_image_factory.title",
    ca = u"Ampliació estàndard de la galeria d'imatges",
    es = u"Ampliación estándar de la galería de imágenes",
    en = u"Default image gallery close up"
)

translations.define(
    "woost.initialization.default_thumbnail_image_factory.title",
    ca = u"Miniatura estàndard de la galeria d'imatges",
    es = u"Miniatura estándar de la galería de imágenes",
    en = u"Default image gallery thumbnail"
)

translations.define(
    "woost.initialization.collage_image_factory.title",
    ca = u"Peça de collage",
    es = u"Pieza de collage",
    en = u"Collage piece"
)

#------------------------------------------------------------------------------

translations.define(
    "woost.authenticationscheme.AuthenticationFailedError-instance",
    ca = u"Usuari o contrasenya incorrectes",
    es = u"Usuario o contraseña incorrectos",
    en = u"Incorrect user or password",
    pt = u"O nome de usuário ou palavra-passe não são corretos"
)

translations.define("woost.views.ContentTable sorting header",
    ca = u"Ordenació",
    es = u"Ordenación",
    en = u"Order"
)

translations.define("woost.views.ContentTable grouping header",
    ca = u"Agrupació",
    es = u"Agrupación",
    en = u"Grouping"
)

translations.define("woost.views.ContentTable search header",
    ca = u"Filtres",
    es = u"Filtros",
    en = u"Filters"
)

translations.define("woost.views.ImageGallery.close_button",
    ca = u"Tancar la imatge",
    es = u"Cerrar la imagen",
    en = u"Close image"
)

translations.define("woost.views.ImageGallery.next_button",
    ca = u"Següent",
    es = u"Siguiente",
    en = u"Next"
)

translations.define("woost.views.ImageGallery.previous_button",
    ca = u"Anterior",
    es = u"Anterior",
    en = u"Previous"
)

translations.define("woost.views.ImageGallery.loading_sign",
    ca = u"Carregant la imatge",
    es = u"Cargando la imagen",
    en = u"Loading image"
)

translations.define("woost.views.ImageGallery.original_image_link",
    ca = u"Descarregar l'original",
    es = u"Descargar el original",
    en = u"Download the original"
)

# Dialog
#------------------------------------------------------------------------------
translations.define("woost.views.Dialog.close_dialog_button",
    ca = u"Tancar la finestra",
    es = u"Cerrar la ventana",
    en = u"Close this window"
)

# Content views
#------------------------------------------------------------------------------
translations.define("woost.content_views.flat",
    ca = u"Llistat",
    es = u"Listado",
    en = u"Listing"
)

translations.define("woost.content_views.tree",
    ca = u"Arbre",
    es = u"Árbol",
    en = u"Tree"
)

translations.define("woost.content_views.thumbnails",
    ca = u"Miniatures",
    es = u"Miniaturas",
    en = u"Grid"
)

translations.define("woost.content_views.calendar",
    ca = u"Calendari",
    es = u"Calendario",
    en = u"Calendar"
)

translations.define("woost.views.CalendarContentView current year",
    ca = u"Any actual",
    es = u"Año actual",
    en = u"Current year"
)

translations.define("woost.views.CalendarContentView previous year",
    ca = u"Any anterior",
    es = u"Año anterior",
    en = u"Previous year"
)

translations.define("woost.views.CalendarContentView next year",
    ca = u"Any següent",
    es = u"Año siguiente",
    en = u"Next year"
)

translations.define("woost.views.CalendarContentView current month",
    ca = u"Mes actual",
    es = u"Mes actual",
    en = u"Current month"
)

translations.define("woost.views.CalendarContentView previous month",
    ca = u"Mes anterior",
    es = u"Mes anterior",
    en = u"Previous month"
)

translations.define("woost.views.CalendarContentView next month",
    ca = u"Mes següent",
    es = u"Mes siguiente",
    en = u"Next month"
)

translations.define("woost.views.CalendarContentView select year layout",
    ca = u"Vista de l'any",
    es = u"Vista del año",
    en = u"Year view"
)

translations.define(
    "woost.views.CalendarContentView ongoing items message",
    ca = u"Elements en curs:",
    es = u"Elementos en curso:",
    en = u"Ongoing items:"
)

# BackOfficeFieldsView
#------------------------------------------------------------------------------
translations.define(
    "woost.views.BackOfficeFieldsView.translations_dropdown",
    ca = u"Traduccions",
    es = u"Traducciones",
    en = u"Translations"
)

translations.define(
    "woost.views.BackOfficeFieldsView.translations_dropdown.shortcut",
    ca = u"t",
    es = u"t",
    en = u"t"
)

translations.define(
    "woost.views.BackOfficeFieldsView.translations_dropdown.submit_button",
    ca = u"Aplicar",
    es = u"Aplicar",
    en = u"Apply"
)

# ItemTranslationsSelector
#------------------------------------------------------------------------------
translations.define(
    "woost.views.ItemTranslationsSelector.selection_controls_label",
    ca = u"Seleccionar:",
    es = u"Seleccionar:",
    en = u"Select:"
)

translations.define(
    "woost.views.ItemTranslationsSelector.select_all_link",
    ca = u"Tots",
    es = u"Todos",
    en = u"All"
)

translations.define(
    "woost.views.ItemTranslationsSelector.select_none_link",
    ca = u"Cap",
    es = u"Ninguno",
    en = u"None"
)

translations.define(
    "woost.views.ItemTranslationsSelector.available_languages_section.heading",
    ca = u"Idiomes disponibles",
    es = u"Idiomas disponibles",
    en = u"Available languages"
)

translations.define(
    "woost.views.ItemTranslationsSelector.defined_languages_section.heading",
    ca = u"Traduccions definides",
    es = u"Traducciones definidas",
    en = u"Defined translations"
)

translations.define(
    "woost.views.ItemTranslationsSelector.add_translation_button",
    ca = u"Afegir",
    es = u"Añadir",
    en = u"Add"
)

translations.define(
    "woost.views.ItemTranslationsSelector.add_translation_button.shortcut",
    ca = u"a",
    es = u"a",
    en = u"a"
)

translations.define(
    "woost.views.ItemTranslationsSelector.delete_translation_button",
    ca = u"Eliminar",
    es = u"Eliminar",
    en = u"Delete"
)

translations.define(
    "woost.views.ItemTranslationsSelector.delete_translation_button.shortcut",
    ca = u"e",
    es = u"e",
    en = u"d"
)

translations.define(
    "woost.views.ItemTranslationsSelector.show_translation_button",
    ca = u"Mostrar",
    es = u"Mostrar",
    en = u"Show"
)

translations.define(
    "woost.views.ItemTranslationsSelector.show_translation_button.shortcut",
    ca = u"m",
    es = u"m",
    en = u"s"
)

translations.define(
    "woost.views.ItemTranslationsSelector.hide_translation_button",
    ca = u"Ocultar",
    es = u"Ocultar",
    en = u"Hide"
)

translations.define(
    "woost.views.ItemTranslationsSelector.hide_translation_button.shortcut",
    ca = u"o",
    es = u"o",
    en = u"h"
)

# Edit form
#------------------------------------------------------------------------------
translations.define("BackOfficeEditForm.properties",
    ca = u"Propietats",
    es = u"Propiedades",
    en = u"Properties"
)

translations.define("BackOfficeEditForm.relations",
    ca = u"Relacions",
    es = u"Relaciones",
    en = u"Relations"
)

translations.define("BackOfficeEditForm.change_password",
    ca = u"Canviar la contrasenya",
    es = u"Cambiar la contraseña",
    en = u"Change password"
)

translations.define("BackOfficeEditForm.password_confirmation",
    ca = u"Confirmar la contrasenya",
    es = u"Confirmar la contraseña",
    en = u"Confirm password"
)

translations.define(
    "woost.controllers.backoffice.usereditnode."
    "PasswordConfirmationError-instance",
    ca = u"Les contrasenyes no coincideixen",
    es = u"Las contraseñas no coinciden",
    en = u"Passwords don't match",
    pt = u"As palavras-passe não são iguais"
)

translations.define(
    "woost.controllers.backoffice.editstack.ItemSavedNotification-instance",
    ca = lambda instance:
        (
            u"S'ha creat l'element <strong>%s</strong>"
            if instance.item_is_new
            else u"Canvis a <strong>%s</strong> desats"
        )
        % translations(instance.item),
    es = lambda instance:
        (
            u"Se ha creado el elemento <strong>%s</strong>"
            if instance.item_is_new
            else u"Cambios en <strong>%s</strong> guardados"
        )
        % translations(instance.item),
    en = lambda instance:
        (
            u"New item <strong>%s</strong> stored"
            if instance.item_is_new
            else u"Saved changes to <strong>%s</strong>"
        )
        % translations(instance.item)
)

translations.define(
    "woost.views.BackOfficeItemView pending changes warning",
    ca = u"Hi ha canvis pendents de desar. Si abandones el formulari d'edició "
        u"els canvis es perdran.",
    es = u"Hay cambios pendientes de guardar. Si abandonas el formulario de "
        u"edición los cambios se perderán.",
    en = u"There are unsaved changes. If you navigate away from the edit form "
        u"your modifications will be lost."
)

translations.define(
    "woost.controllers.backoffice.basebackofficecontroller."
    "EditStateLostError",
    ca = u"La sessió d'edició en que estaves treballant s'ha perdut.",
    es = u"La sesión de edición en que estabas trabajando se ha perdido.",
    en = u"The edit session you were working on has been lost."
)

translations.define("woost.cache_invalidated_notice",
    ca = lambda subset:
        u"S'ha netejat el cache de %s"
        % (
            u"tota la web" if subset is None
            else plural2(len(subset), "%d elements" % len(subset), "1 element")
        ),
    es = lambda subset:
        u"Se ha limpiado el cache de %s"
        % (
            u"toda la web" if subset is None
            else plural2(len(subset), "%d elementos" % len(subset), "1 elemento")
        ),
    en = lambda subset:
        u"Cleared the cache for %s"
        % (
            u"the whole web" if subset is None
            else plural2(len(subset), "%d elements" % len(subset), "1 element")
        )
)

translations.define("woost.duplicate_created_notice",
    ca = u"S'ha creat el duplicat. Assegura't de revisar-lo i editar-lo com "
         u"correspongui.",
    es = u"Se ha creado el duplicado. Asegurate de revisarlo y modificarlo "
         u"como corresponda.",
    en = u"Your duplicated element is ready. Make sure to review and modify "
         u"it as necessary."
)

translations.define("woost.views.BaseView alternate language link",
    ca = lambda lang: u"Versió en " + translations("locale", locale = lang),
    es = lambda lang: u"Versión en " + translations("locale", locale = lang),
    en = lambda lang: translations("locale", locale = lang) + u" version"
)

translations.define("woost.views.StandardView.navigation_title",
    ca = u"Menú principal",
    es = u"Menú principal",
    en = u"Main navigation"
)

translations.define("woost.views.StandardView attachment icon description",
    ca = u"Icona",
    es = u"Icono",
    en = u"Icon"
)

translations.define("woost.views.StandardView fallback language notice",
    ca = lambda fallback:
        u"Aquesta pàgina no es troba disponible en català. Et mostrem "
        u"la seva versió en %s." % translations(fallback).lower(),
    es = lambda fallback:
        u"Esta página no se encuentra disponible en español. Te "
        u"mostramos su versión en %s." % translations(fallback).lower(),
    en = lambda fallback:
        u"This page is not available in english. Its %s version is "
        u"shown instead." % translations(fallback).lower()
)

translations.define("woost.views.StandardView.phone_number",
    ca = u"Tel",
    es = u"Tel",
    en = u"Telephone"
)

translations.define("UploadFilesForm.upload",
    ca = u"Fitxer ZIP",
    es = u"Fichero ZIP",
    en = u"ZIP file"
)

translations.define(
    "UploadFilesForm.upload.mime_type-error: cocktail.schema.exceptions.EnumerationError",
    ca = u"El fitxer indicat no és un fitxer ZIP",
    es = u"El fichero indicado no es un fichero ZIP",
    en = u"The selected file is not a ZIP file"
)

translations.define("woost.views.BackOfficeUploadFilesView.success_notice",
    ca = lambda count: u"S'ha importat un total de <strong>%d</strong> %s:"
        % (count, plural2(count, u"fitxer", u"fitxers")),
    es = lambda count: u"Se han importado un total de <strong>%d</strong> %s:"
        % (count, plural2(count, u"fichero", u"ficheros")),
    en = lambda count: u"Uploaded <strong>%d</strong> %s:"
        % (count, plural2(count, u"file", u"files"))
)

translations.define("woost.views.BackOfficeUploadFilesView.upload_another",
    ca = u"Importar més fitxers",
    es = u"Importar más ficheros",
    en = u"Import more files"
)

# Type groups
#------------------------------------------------------------------------------
translations.define("woost.type_groups.misc",
    ca = u"Miscel·lània",
    es = u"Miscelanea",
    en = u"Miscellany"
)

translations.define("woost.type_groups.publishable",
    ca = u"Elements publicables",
    es = u"Elementos publicables",
    en = u"Publishable items"
)

translations.define("woost.type_groups.document",
    ca = u"Documents",
    es = u"Documentos",
    en = u"Documents"
)

translations.define("woost.type_groups.resource",
    ca = u"Recursos",
    es = u"Recursos",
    en = u"Resources"
)

translations.define("woost.type_groups.setup",
    ca = u"Administració",
    es = u"Administración",
    en = u"Setup"
)

translations.define("woost.type_groups.customization",
    ca = u"Personalització",
    es = u"Personalización",
    en = u"Customization"
)

translations.define("woost.type_groups.users",
    ca = u"Usuaris i permisos",
    es = u"Usuarios y permisos",
    en = u"Users and permissions"
)

translations.define("woost.type_groups.blocks.content",
    ca = u"Contingut",
    es = u"Contenido",
    en = u"Content"
)

translations.define("woost.type_groups.blocks.layout",
    ca = u"Disposició",
    es = u"Disposición",
    en = u"Layout"
)

translations.define("woost.type_groups.blocks.listings",
    ca = u"Llistats",
    es = u"Listados",
    en = u"Listings"
)

translations.define("woost.type_groups.blocks.social",
    ca = u"Xarxes socials",
    es = u"Redes sociales",
    en = u"Social networks"
)

translations.define("woost.type_groups.blocks.forms",
    ca = u"Formularis",
    es = u"Formularios",
    en = u"Forms"
)

translations.define("woost.type_groups.blocks.custom",
    ca = u"Avançats",
    es = u"Avanzados",
    en = u"Custom"
)

# Item
#------------------------------------------------------------------------------
translations.define("Item",
    ca = u"Element genèric",
    es = u"Elemento genérico",
    en = u"Generic element"
)

translations.define("Item-plural",
    ca = u"Elements genèrics",
    es = u"Elementos genéricos",
    en = u"Generic elements"
)

translations.define("Item-menu",
    ca = u"Tots els elements del web",
    es = u"Todos los elementos de la web",
    en = u"All elements"
)

translations.define("Item-none",
    ca = u"Cap",
    es = u"Ninguno",
    en = u"None"
)

translations.define("Item.administration",
    ca = u"Administració",
    es = u"Administración",
    en = u"Administration"
)

translations.define("Item.id",
    ca = u"ID",
    es = u"ID",
    en = u"ID"
)

translations.define("Item.qname",
    ca = u"Nom qualificat",
    es = u"Nombre cualificado",
    en = u"Qualified name"
)

translations.define("Item.global_id",
    ca = u"Identificador global",
    es = u"Identificador global",
    en = u"Global identifier"
)

translations.define("Item.synchronizable",
    ca = u"Sincronitzable",
    es = u"Sincronizable",
    en = u"Synchronizable"
)

translations.define("Item.synchronizable-explanation",
    ca = u"Indica si l'objecte es tindrà en compte a l'hora de sincronitzar "
         u"les dades de dues còpies del lloc web.",
    es = u"Indica si el objeto se tendrá en cuenta a la hora de sincronizar "
         u"los datos de dos copias del sitio web.",
    en = u"Indicates wether the object will be taken into account when "
         u"synchronizing data across copies of the site."
)

translations.define("Item.author",
    ca = u"Autor",
    es = u"Autor",
    en = u"Author"
)

translations.define("Item.changes",
    ca = u"Canvis",
    es = u"Cambios",
    en = u"Changes"
)

translations.define("Item.creation_time",
    ca = u"Data de creació",
    es = u"Fecha de creación",
    en = u"Creation date"
)

translations.define("Item.last_update_time",
    ca = u"Última modificació",
    es = u"Última modificación",
    en = u"Last updated"
)

translations.define("Item.last_translation_update_time",
    ca = u"Última modificació de la traducció",
    es = u"Última modificación de la traducción",
    en = u"Translation last update"
)

# Configuration
#------------------------------------------------------------------------------
translations.define("Configuration",
    ca = u"Configuració",
    es = u"Configuración",
    en = u"Configuration"
)

translations.define("Configuration-plural",
    ca = u"Configuració",
    es = u"Configuración",
    en = u"Configuration"
)

translations.define("Configuration.publication",
    ca = u"Publicació",
    es = u"Publicación",
    en = u"Publication"
)

translations.define("Configuration.publication.pages",
    ca = u"Pàgines especials",
    es = u"Páginas especiales",
    en = u"Special pages"
)

translations.define("Configuration.publication.maintenance",
    ca = u"Manteniment",
    es = u"Mantenimiento",
    en = u"Maintenance"
)

translations.define("Configuration.language",
    ca = u"Idioma",
    es = u"Idioma",
    en = u"Language"
)

translations.define("Configuration.media",
    ca = u"Multimèdia",
    es = u"Multimedia",
    en = u"Media"
)

translations.define("Configuration.media.images",
    ca = u"Imatges",
    es = u"Imagenes",
    en = u"Images"
)

translations.define("Configuration.media.video",
    ca = u"Vídeo",
    es = u"Video",
    en = u"Video"
)

translations.define("Configuration.rendering",
    ca = u"Processat d'imatges",
    es = u"Procesado de imágenes",
    en = u"Image processing"
)

translations.define("Configuration.services",
    ca = u"Serveis",
    es = u"Servicios",
    en = u"Services"
)

translations.define("Configuration.system",
    ca = u"Sistema",
    es = u"Sistema",
    en = u"System"
)

translations.define("Configuration.system.smtp",
    ca = u"Servidor SMTP",
    es = u"Servidor SMTP",
    en = u"SMTP server"
)

translations.define("Configuration.common_blocks",
    ca = u"Blocs comuns",
    es = u"Bloques comunes",
    en = u"Common blocks"
)

translations.define("Configuration.websites",
    ca = u"Pàgines web",
    es = u"Páginas web",
    en = u"Websites"
)

translations.define("Configuration.caching_policies",
    ca = u"Polítiques de cache",
    es = u"Políticas de cache",
    en = u"Caching policies"
)

translations.define("Configuration.login_page",
    ca = u"Pàgina d'autenticació",
    es = u"Página de autenticación",
    en = u"Authentication page"
)

translations.define("Configuration.generic_error_page",
    ca = u"Pàgina d'error genèric",
    es = u"Página de error genérico",
    en = u"Generic error page"
)

translations.define("Configuration.not_found_error_page",
    ca = u"Pàgina no trobada",
    es = u"Página no encontrada",
    en = u"Not found error page",
    pt = u"Página não encontrada"
)

translations.define("Configuration.forbidden_error_page",
    ca = u"Pàgina d'error per accés restringit",
    es = u"Página de error por acceso restringido",
    en = u"Access forbidden page"
)

translations.define("Configuration.down_for_maintenance",
    ca = u"Lloc aturat per manteniment",
    es = u"Sitio parado por mantenimiento",
    en = u"Site down for maintenance"
)

translations.define("Configuration.maintenance_page",
    ca = u"Pàgina a mostrar durant el manteniment",
    es = u"Página a mostrar durante el mantenimiento",
    en = u"Service unavailable page"
)

translations.define("Configuration.maintenance_addresses",
    ca = u"Adreces IP que ignoren el mode de manteniment",
    es = u"Direcciones IP que ignoran el modo de mantenimiento",
    en = u"IP addresses that ignore maintenance mode"
)

translations.define("Configuration.languages",
    ca = u"Idiomes",
    es = u"Idiomas",
    en = u"Languages"
)

translations.define("Configuration.languages-explanation",
    ca = u"Llistat d'idiomes als que es pot traduïr el contingut. Cada "
         u"idioma s'indica mitjançant el seu codi ISO de dues lletres.",
    es = u"Listado de idiomas a los que se puede traducir el contenido. Cada "
         u"idioma se indica mediante su código ISO de dos letras.",
    en = u"Languages that content can be translated to. Each language is "
         u"specified using its two letter ISO code."
)

translations.define("Configuration.published_languages",
    ca = u"Idiomes publicats",
    es = u"Idiomas publicados",
    en = u"Published languages"
)

translations.define("Configuration.published_languages-explanation",
    ca = u"Limita els idiomes publicats al subconjunt indicat. Deixar en "
         u"blanc per permetre la publicació en qualsevol dels idiomes "
         u"disponibles.",
    es = u"Limita los idiomas publicados al subconjunto indicado. Dejar en "
         u"blanco para permitir la publicación en cualquiera de los idiomas "
         u"disponibles.",
    en = u"Limits publication to the indicated subset of languages. Leave "
         u"blank to allow publishing in any of the available languages."
)

translations.define("Configuration.virtual_languages",
    ca = u"Idiomes virtuals",
    es = u"Idiomas virtuales",
    en = u"Virtual languages"
)

translations.define("Configuration.virtual_languages-explanation",
    ca = u"Indica els idiomes que no es publiquen mai directament, si no que "
         u"només actuen com a base per a altres idiomes.",
    es = u"Indica los idiomas que no se publican nunca directamente, si no "
         u"que solo actuan como base para otros idiomas.",
    en = u"Establishes a set of languages that will never be directly "
         u"published, and will be used instead as a base for other languages."
)

translations.define("Configuration.default_language",
    ca = u"Idioma per defecte",
    es = u"Idioma por defecto",
    en = u"Default language"
)

translations.define("Configuration.heed_client_language",
    ca = u"Respectar les preferències d'idioma del navegador",
    es = u"Respetar las preferencias de idioma del navegador",
    en = u"Heed the language preferences from the browser"
)

translations.define("Configuration.fallback_languages",
    ca = u"Idiomes substitutius",
    es = u"Idiomas sustitutivos",
    en = u"Fallback languages"
)

translations.define("Configuration.backoffice_language",
    ca = u"Idioma per defecte de la interfície d'edició",
    es = u"Idioma por defecto de la interfaz de edición",
    en = u"Default language for the backoffice"
)

translations.define("Configuration.backoffice_language_chain",
    ca = u"Idiomes a utilitzar en descriure el contingut",
    es = u"Idiomas a utilizar al describir el contenido",
    en = u"Languages to use when describing content"
)

translations.define("Configuration.renderers",
    ca = u"Pintadors",
    es = u"Pintadores",
    en = u"Renderers"
)

translations.define("Configuration.renderers-explanation",
    ca = u"Components encarregats de produïr una imatge representativa a "
         u"partir d'un tipus de contingut específic (imatges, PDFs, vídeos, "
         u"etc).",
    es = u"Componentes encargados de producir una imagen representativa a "
         u"partir de un tipo de contenido específico (imágenes, PDFs, "
         u"videos, etc).",
    en = u"Components tasked with producing images for different kinds of "
         u"content (ie. image files, PDF documents, videos, etc)."
)

translations.define("Configuration.image_factories",
    ca = u"Processadors d'imatges",
    es = u"Procesadores de imágenes",
    en = u"Image factories"
)

translations.define("Configuration.image_factories-explanation",
    ca = u"Les diferents variants de redimensionat i efectes que "
         u"s'apliquen a les imatges de la web.",
    es = u"Las distintas variaciones de redimensionado y efectos que "
         u"se aplican a las imágenes de la web.",
    en = u"The different resizing and transformation effects applied "
         u"to the site's images."
)

translations.define("Configuration.video_player_settings",
    ca = u"Opcions de reproductor de vídeo",
    es = u"Opciones de reproductor de video",
    en = u"Video player settings"
)

translations.define("Configuration.timezone",
    ca = u"Zona horària",
    es = u"Zona horaria",
    en = u"Timezone"
)

translations.define("Configuration.smtp_host",
    ca = u"Adreça del servidor SMTP",
    es = u"Dirección del servidor SMTP",
    en = u"SMTP host"
)

translations.define("Configuration.smtp_user",
    ca = u"Compte d'usuari del servidor SMTP",
    es = u"Cuenta de usuario del servidor SMTP",
    en = u"SMTP server user account"
)

translations.define("Configuration.smtp_password",
    ca = u"Contrasenya del servidor SMTP",
    es = u"Contraseña de usuario del servidor SMTP",
    en = u"SMTP server password"
)

translations.define("Configuration.triggers",
    ca = u"Disparadors",
    es = u"Disparadores",
    en = u"Triggers"
)

translations.define("Configuration.triggers-explanation",
    ca = u"Permet programar accions que s'activin quan es produeixin canvis "
         u"al contingut.",
    es = u"Permite programar acciones que se activen cuando se produzcan "
         u"cambios en el contenido",
    en = u"Program actions that will be activated when the site's content "
         u"changes."
)

# Website
#------------------------------------------------------------------------------
translations.define("Website",
    ca = u"Lloc web",
    es = u"Sitio web",
    en = u"Website"
)

translations.define("Website-plural",
    ca = u"Llocs web",
    es = u"Sitios web",
    en = u"Websites"
)

translations.define("Website.website",
    ca = u"Lloc web",
    es = u"Sitio web",
    en = u"Website"
)

translations.define("Website.contact",
    ca = u"Contacte",
    es = u"Contacto",
    en = u"Contact"
)

translations.define("Website.publication",
    ca = u"Publicació",
    es = u"Publicación",
    en = u"Publication"
)

translations.define("Website.publication.pages",
    ca = u"Pàgines especials",
    es = u"Páginas especiales",
    en = u"Special pages"
)

translations.define("Website.publication.maintenance",
    ca = u"Manteniment",
    es = u"Mantenimiento",
    en = u"Maintenance"
)

translations.define("Website.publication.https",
    ca = u"HTTPS",
    es = u"HTTPS",
    en = u"HTTPS"
)

translations.define("Website.language",
    ca = u"Idioma",
    es = u"Idioma",
    en = u"Language"
)

translations.define("Website.services",
    ca = u"Serveis",
    es = u"Servicios",
    en = u"Services"
)

translations.define("Website.specific_content",
    ca = u"Contingut específic",
    es = u"Contenido específico",
    en = u"Specific content"
)

translations.define("Website.site_name",
    ca = u"Nom del lloc",
    es = u"Nombre del sitio",
    en = u"Site name"
)

translations.define("Website.logo",
    ca = u"Logotip",
    es = u"Logotipo",
    en = u"Logo"
)

translations.define("Website.icon",
    ca = u"Icona",
    es = u"Icono",
    en = u"Icon"
)

translations.define("Website.keywords",
    ca = u"Paraules clau",
    es = u"Palabras clave",
    en = u"Keywords"
)

translations.define("Website.description",
    ca = u"Descripció",
    es = u"Descripción",
    en = u"Description"
)

translations.define("Website.hosts",
    ca = u"Dominis",
    es = u"Dominios",
    en = u"Hosts"
)

translations.define("Website.hosts-explanation",
    ca = u"La llista de dominis que han d'associar-se a aquesta web. "
         u"Poden utilitzar-se comodins (per exemple, *.foo.com).",
    es = u"La lista de dominios que deben asociarse a esta web. Pueden "
         u"utilizarse comodines (por ejemplo, *.foo.com).",
    en = u"The list of domains that can be associated to this website. Can "
         u"use wildcard expressions (such as *.foo.com)."
)

translations.define("Website.organization_name",
    ca = u"Nom de l'entitat",
    es = u"Nombre de la entidad",
    en = u"Entity name"
)

translations.define("Website.organization_url",
    ca = u"URL de l'entitat",
    es = u"URL de la entidad",
    en = u"Entity URL"
)

translations.define("Website.address",
    ca = u"Adreça",
    es = u"Dirección",
    en = u"Address"
)

translations.define("Website.town",
    ca = u"Localitat",
    es = u"Localidad",
    en = u"Town"
)

translations.define("Website.region",
    ca = u"Regió",
    es = u"Región",
    en = u"Region"
)

translations.define("Website.postal_code",
    ca = u"Codi postal",
    es = u"Código postal",
    en = u"Postal code"
)

translations.define("Website.country",
    ca = u"País",
    es = u"País",
    en = u"Country"
)

translations.define("Website.phone_number",
    ca = u"Telèfon",
    es = u"Teléfono",
    en = u"Phone number"
)

translations.define("Website.fax_number",
    ca = u"Fax",
    es = u"Fax",
    en = u"Fax"
)

translations.define("Website.email",
    ca = u"Correu electrònic",
    es = u"Correo electrónico",
    en = u"Email"
)

translations.define("Website.home",
    ca = u"Pàgina d'inici",
    es = u"Página de inicio",
    en = u"Home page"
)

translations.define("Website.login_page",
    ca = u"Pàgina d'autenticació",
    es = u"Página de autenticación",
    en = u"Authentication page"
)

translations.define("Website.generic_error_page",
    ca = u"Pàgina d'error genèric",
    es = u"Página de error genérico",
    en = u"Generic error page"
)

translations.define("Website.not_found_error_page",
    ca = u"Pàgina no trobada",
    es = u"Página no encontrada",
    en = u"Not found error page"
)

translations.define("Website.forbidden_error_page",
    ca = u"Pàgina d'error per accés restringit",
    es = u"Página de error por acceso restringido",
    en = u"Access forbidden page"
)

translations.define("Website.down_for_maintenance",
    ca = u"Lloc aturat per manteniment",
    es = u"Sitio parado por mantenimiento",
    en = u"Site down for maintenance"
)

translations.define("Website.maintenance_page",
    ca = u"Pàgina a mostrar durant el manteniment",
    es = u"Página a mostrar durante el mantenimiento",
    en = u"Service unavailable page"
)

translations.define("Website.https_policy",
    ca = u"Política de HTTPS",
    es = u"Política de HTTPS",
    en = u"HTTPS policy"
)

translations.define("Website.https_policy=always",
    ca = u"Habilitar a totes les pàgines",
    es = u"Habilitar en todas las páginas",
    en = u"Enable for all pages"
)

translations.define("Website.https_policy=never",
    ca = u"Deshabilitar a totes les pàgines",
    es = u"Deshabilitar en todas las páginas",
    en = u"Disable for all pages"
)

translations.define("Website.https_policy=per_page",
    ca = u"Decidir-ho a cada pàgina",
    es = u"Decidirlo en cada página",
    en = u"Decide on a per-page basis"
)

translations.define("Website.https_persistence",
    ca = u"Preservar HTTPS entre peticions",
    es = u"Preservar HTTPS entre peticiones",
    en = u"Persist HTTPS navigation across requests"
)

translations.define("Website.https_persistence-explanation",
    ca = u"Aquesta opció només tindrà efecte si la <em>Política "
         u"d'HTTPS</em> s'estableix a <em>Decidir a cada pàgina</em>.",
    es = u"Esta opción solo tendrá efecto si la <em>Política "
         u"de HTTPS</em> se establece a <em>Decidir en cada página</em>.",
    en = u"This option will only be taken into account if "
         u"<em>HTTPS policy</em> is set to <em>Decide on a per-page "
         u"basis</em>."
)

translations.define("Website.default_language",
    ca = u"Idioma per defecte",
    es = u"Idioma por defecto",
    en = u"Default language"
)

translations.define("Website.heed_client_language",
    ca = u"Respectar les preferències d'idioma del navegador",
    es = u"Respetar las preferencias de idioma del navegador",
    en = u"Heed the language preferences from the browser"
)

translations.define("Website.published_languages",
    ca = u"Idiomes publicats",
    es = u"Idiomas publicados",
    en = u"Published languages"
)

translations.define("Website.published_languages-explanation",
    ca = u"Limita els idiomes publicats al subconjunt indicat. Deixar en "
         u"blanc per permetre la publicació en qualsevol dels idiomes "
         u"disponibles.",
    es = u"Limita los idiomas publicados al subconjunto indicado. Dejar en "
         u"blanco para permitir la publicación en cualquiera de los idiomas "
         u"disponibles.",
    en = u"Limits publication to the indicated subset of languages. Leave "
         u"blank to allow publishing in any of the available languages."
)

translations.define("woost.views.LoginFormView.main",
    ca = u"""L'accés a aquesta secció del web està restringit. Per favor,
            introdueix les teves credencials d'usuari per continuar.""",
    es = u"""El acceso a esta sección del sitio está restringido. Por favor,
            introduce tus credenciales de usuario para continuar.""",
    en = u"""Access to this part of the website is restricted. Please, introduce
            your user credentials to proceed."""
)

translations.define("woost.views.LoginForm.forgot_password_link",
    ca = u"He oblidat la contrasenya",
    es = u"He olvidado la contraseña",
    en = u"I forgot my password",
    pt = u"Esqueceu a sua chave de acesso?"
)

translations.define("woost.views.LoginForm.submit_button",
    ca = u"Entrar",
    es = u"Entrar",
    en = u"Enter"
)

# SiteInstallation
#------------------------------------------------------------------------------
translations.define("SiteInstallation",
    ca = u"Instal·lació del lloc web",
    es = u"Instalación del sitio web",
    en = u"Site installation"
)

translations.define("SiteInstallation-plural",
    ca = u"Instal·lacions del lloc web",
    es = u"Instalaciones del sitio web",
    en = u"Site installations"
)

translations.define("SiteInstallation.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("SiteInstallation.url",
    ca = u"URL",
    es = u"URL",
    en = u"URL"
)

translations.define("SiteInstallation.synchronization_user",
    ca = u"Usuari per la sincronització",
    es = u"Usuario para la sincronización",
    en = u"Synchronization user"
)

translations.define("SiteInstallation.synchronization_password",
    ca = u"Contrasenya per la sincronització",
    es = u"Contraseña para la sincronización",
    en = u"Synchronization password"
)

# CachingPolicy
#------------------------------------------------------------------------------
translations.define("CachingPolicy",
    ca = u"Política de cache",
    es = u"Política de cache",
    en = u"Caching policy"
)

translations.define("CachingPolicy-plural",
    ca = u"Polítiques de cache",
    es = u"Políticas de cache",
    en = u"Caching policies"
)

translations.define("CachingPolicy.description",
    ca = u"Descripció",
    es = u"Descripción",
    en = u"Description"
)

translations.define("CachingPolicy.important",
    ca = u"Important",
    es = u"Importante",
    en = u"Important"
)

translations.define("CachingPolicy.important-explanation",
    ca = u"Indica que la regla s'aplica abans que la resta.",
    es = u"Indica que la regla se aplica antes que el resto.",
    en = u"Indicates that this rule should be applied before the rest."
)

translations.define("CachingPolicy.cache_enabled",
    ca = u"Cache habilitat",
    es = u"Cache habilitado",
    en = u"Cache enabled"
)

translations.define("CachingPolicy.cache_enabled-explanation",
    ca = u"Si s'habilita el cache, els elements sol·licitats pels usuaris "
         u"només són reprocessats quan han estat modificats. Això millora "
         u"notablement el rendiment, però per contra no garanteix que el "
         u"contingut que es mostra estigui actualitzat a la última "
         u"versió.",
    es = u"Si se habilita el cache, los elementos solicitados por los "
         u"usuarios solo son procesados si han sido modificados. Esto "
         u"mejora notablemente el rendimiento, pero por contra no "
         u"garantiza que el contenido que se muestra a los usuarios esté "
         u"actualizado a la última versión.",
    en = u"Enabling caching for this item will cause the application to "
         u"only process items if they have been modified. This can "
         u"greatly increase performance, at the expense of being unable "
         u"to guarantee that users are served the latest version of the "
         u"content."
)

translations.define("CachingPolicy.server_side_cache",
    ca = u"Cache de servidor habilitat",
    es = u"Cache de servidor habilitado",
    en = u"Server side cache enabled"
)

translations.define("CachingPolicy.server_side_cache-explanation",
    ca = u"Habilitar per mantenir el contingut publicable de l'element "
         u"en memòria. Això accelera el temps de resposta, però "
         u"augmenta els recursos consumits per l'aplicació.",
    es = u"Habilitar para mantener el contenido publicable del elemento "
         u"en memoria. Esto acelera los tiempos de respuesta, pero "
         u"aumenta los recursos consumidos por la aplicación.",
    en = u"Enable to maintain the item's rendered content in memory. This "
         u"minimizes response times, but increases the amount of memory "
         u"consumed by the application."
)

translations.define("CachingPolicy.expiration_expression",
    ca = u"Expiració del cache",
    es = u"Expiración del cache",
    en = u"Cache expiration"
)

translations.define("CachingPolicy.expiration_expression-explanation",
    ca = u"""
        <p>
            Fragment de codi Python que determina la duració de les entrades
            de cache generades per aquesta política.
        </p>
        <details>
            <summary>Detalls</summary>
            <p>
                Si el camp es deixa en blanc es desactiva l'expiració de les
                entrades, que es mantindran actives fins que s'invalidin per
                altres vies (com ara una actualització de l'<em>última
                modificació</em> de l'element publicable).
            </p>
            <p>
                L'expiració s'estableix amb una variable <em>expiration</em>, que pot
                expressar-se utilitzant qualsevol dels tipus següents:
            </p>
            <dl>
                <dt>int</dt>
                <dd>Vigència de l'entrada, en minuts.</dd>
                <dt><a href="http://docs.python.org/2/library/datetime.html#timedelta-objects">timedelta</a></dt>
                <dd>Vigència de l'entrada, expressada en diferents unitats (minuts,
                hores, dies, etc).</dd>
                <dt><a href="http://docs.python.org/2/library/datetime.html#datetime-objects">datetime</a></dt>
                <dd>Data exacta en que l'entrada es considerarà expirada.</dd>
                <dt>None</dt>
                <dd>Duració sense determinar, l'entrada no expirarà
                automàticament.</dd>
            </dl>
            <p>
                L'expressió rep una variable <em>publishable</em> (la
                referència a l'element publicable al que s'aplica la política
                de cache), així com referències a les classes
                <em>datetime</em> i <em>timedelta</em> (com a conveniència,
                per no haver-les d'importar explícitament).
            </p>
        </details>
        """,
    es = u"""
        <p>
            Fragmento de código Python que determina la duración de las
            entradas de cache generadas por esta política.
        </p>
        <details>
            <summary>Detalles</summary>
            <p>
                Si el campo se deja en blanco se desactiva la expiración de
                las entradas, que se mantendrán activas hasta que se invaliden
                por otras vías (como una actualización de la <em>última
                modificación</em> del elemento publicable).
            </p>
            <p>
                La expiración se establece con una variable
                <em>expiration</em>, que puede expresarse mediante
                cualquiera de los siguientes tipos:
            </p>
            <dl>
                <dt>int</dt>
                <dd>Vigencia de la entrada, en minutos.</dd>
                <dt><a href="http://docs.python.org/2/library/datetime.html#timedelta-objects">timedelta</a></dt>
                <dd>Vigencia de la entrada, expresada en distintas unidades
                (minutos, horas, días, etc).</dd>
                <dt><a href="http://docs.python.org/2/library/datetime.html#datetime-objects">datetime</a></dt>
                <dd>Fecha exacta en que la entrada se considerará expirada.</dd>
                <dt>None</dt>
                <dd>Duración sin determinar, la entrada no expirará
                automáticamente.</dd>
            </dl>
            <p>
                La expresión recibe una variable <em>publishable</em> (la
                referencia al elemento publicable al que se aplica la política
                de cache), así como referencias a las clases <em>datetime</em>
                y <em>timedelta</em> (como conveniencia, para no tener que
                importar estos tipos explícitamente).
            </p>
        </details>
        """,
    en = u"""
        <p>
            A Python code block that determines the duration of the cache
            entries generated by this caching policy.
        </p>
        <details>
            <summary>Details</summary>
            <p>
                If the field is left blank, cache entries will not expire, and
                they will have to rely on other means in order to be
                invalidated (such as a change in the <em>last update</em> of
                the publishable element).
            </p>
            <p>
                Entry duration is expressed using an <em>expiration</em>
                variable, using any of the following types:
            </p>
            <dl>
                <dt>int</dt>
                <dd>Expresses entry duration in minutes.</dd>
                <dt><a href="http://docs.python.org/2/library/datetime.html#timedelta-objects">timedelta</a></dt>
                <dd>Expresses entry duration using a variety of units (minutes,
                hours, days, etc).</dd>
                <dt><a href="http://docs.python.org/2/library/datetime.html#datetime-objects">datetime</a></dt>
                <dd>Exact date when the entry will expire.</dd>
                <dt>None</dt>
                <dd>Undefined duration, the entry won't expire on its own.</dd>
            </dl>
            <p>
                The expression receives a <em>publishable</em> variable (the
                publishable element that the cached content is being generated
                for), as well as references to the <em>datetime</em> and
                <em>timedelta</em> standard types (as a convenience, to avoid
                having to import them explicitly).
            </p>
        </details>
        """
)

translations.define("CachingPolicy.condition",
    ca = u"Condició",
    es = u"Condición",
    en = u"Condition"
)

translations.define("CachingPolicy.condition-explanation",
    ca = u"Una expressió que especifica les circumstàncies necessàries "
         u"perquè s'apliqui aquesta política de cache.",
    es = u"Una expresión que especifica las circunstancias necesarias "
         u"para que se aplique esta política de cache.",
    en = u"An expression describing the necessary conditions for this "
         u"caching policy to be applied."
)

translations.define("CachingPolicy.cache_key_expression",
    ca = u"Clau de cache",
    es = u"Clave de cache",
    en = u"Cache key"
)

translations.define("CachingPolicy.cache_key_expression-explanation",
    ca = u"Una expressió que determina l'entrada al cache que correspon a la "
         u"petició en curs. Deixar en blanc per utilitzar l'expressió per "
         u"defecte.",
    es = u"Una expresión que determina la entrada en cache que le "
         u"corresponde a la petición en curso. Dejar en blanco para usar la "
         u"expresión por defecto.",
    en = u"An expression that designates which cache entry should be used by "
         u"the active request. Leave blank to use the default expression."
)

translations.define("CachingPolicy.cache_tags_expression",
    ca = u"Etiquetes de cache",
    es = u"Etiquetas de cache",
    en = u"Cache tags"
)

translations.define("CachingPolicy.cache_tags_expression-explanation",
    ca = u"""
        <p>
            Una expressió Python que determina les etiquetes que s'apliquen a
            les entrades de cache generades per aquesta política.
        </p>
        <details>
            <summary>Detalls</summary>
            <p>
                Les etiquetes permeten classificar les entrades de cache, cosa
                que fa possible invalidar-les de forma selectiva. Mitjançant
                aquest mecanisme és possible invalidar totes les entrades de
                cache per un mateix element o idioma. Amb aquesta expressió
                és possible associar les entrades de cache a altres conceptes.
            </p>
            <p>
                Les etiquetes a aplicar s'han d'especificar a través de la
                variable <em>tags</em>. De sortida, aquesta variable consisteix
                en un conjunt (<em>set</em>) que conté les etiquetes retornades
                pel mètode <em>get_cache_tags</em> de l'element pel que s'està
                generant l'entrada al cache.
            </p>
        </details>
        """,
    es = u"""
        <p>
            Una expresión Python que determina las etiquetas que se aplican a
            las entrades de cache generades por esta política.
        </p>
        <details>
            <summary>Detalles</summary>
            <p>
                Las etiquetas permiten clasificar las entradas de cache, cosa
                que hace posible invalidarlas de forma selectiva. Mediante este
                mecanismo es posible invalidar todas las entradas del cache
                para un mismo elemento o idioma. Con esta expresión se pueden
                asociar las entradas a otros conceptos.
            </p>
            <p>
                Las etiquetas a aplicar se especifican a través de la variable
                <em>tags</em>. De salida, la variable consiste en un conjunto
                (<em>set</em>) que contiene las etiquetas devueltas por el
                método <em>get_cache_tags</em> del elemento para el que se está
                generando la entrada de cache.
            </p>
        </details>
        """,
    en = u"""
        <p>
            A Python expression that determines the tags that will be applied
            to the cache entries produced by this caching policy.
        </p>
        <details>
            <summary>Details</summary>
            <p>
                Tags allow the classification of cache entries, which makes it
                possible to selectively invalidate parts of the cache. By
                default, entries are given tags indicating the item that they
                represent, and the language of their content. With this
                expression it is possible to bind cache entries to other
                concepts.
            </p>
            <p>
                The tags to apply are specified through the <em>tags</em>
                variable. Out of the box, this variable will consist of a
                <em>set</em> containing all the tags produced by the
                <em>get_cache_tags</em> method of the item for which the cache
                entry is being generated.
            </p>
        </details>
        """
)

# Publishable
#------------------------------------------------------------------------------
translations.define("Publishable",
    ca = u"Element publicable",
    es = u"Elemento publicable",
    en = u"Publishable element"
)

translations.define("Publishable-plural",
    ca = u"Elements publicables",
    es = u"Elementos publicables",
    en = u"Publishable elements"
)

translations.define("Publishable-menu",
    ca = u"Tots els elements publicables",
    es = u"Todos los elementos publicables",
    en = u"All publishable elements"
)

translations.define("Publishable.meta",
    ca = u"Metadades",
    es = u"Metadatos",
    en = u"Metadata"
)

translations.define("Publishable.presentation",
    ca = u"Presentació",
    es = u"Presentación",
    en = u"Presentation"
)

translations.define("Publishable.presentation.behavior",
    ca = u"Comportament",
    es = u"Comportamiento",
    en = u"Behavior"
)

translations.define("Publishable.presentation.format",
    ca = u"Format",
    es = u"Formato",
    en = u"Format"
)

translations.define("Publishable.navigation",
    ca = u"Navegació",
    es = u"Navegación",
    en = u"Navigation"
)

translations.define("Publishable.publication",
    ca = u"Publicació",
    es = u"Publicación",
    en = u"Publication"
)

translations.define("Publishable.resource_type",
    ca = u"Tipus de recurs",
    es = u"Tipo de recurso",
    en = u"Resource type"
)

translations.define("Publishable.encoding",
    ca = u"Codificació de text",
    es = u"Codificación del texto",
    en = u"Text encoding"
)

translations.define("woost.models.Publishable.resource_type text",
    ca = u"Text",
    es = u"Texto",
    en = u"Text"
)

translations.define("woost.models.Publishable.resource_type image",
    ca = u"Imatge",
    es = u"Imagen",
    en = u"Image"
)

translations.define("woost.models.Publishable.resource_type audio",
    ca = u"Audio",
    es = u"Audio",
    en = u"Audio"
)

translations.define("woost.models.Publishable.resource_type video",
    ca = u"Video",
    es = u"Video",
    en = u"Video"
)

translations.define("woost.models.Publishable.resource_type package",
    ca = u"Paquet",
    es = u"Paquete",
    en = u"Package"
)

translations.define("woost.models.Publishable.resource_type document",
    ca = u"Document",
    es = u"Documento",
    en = u"Document"
)

translations.define("woost.models.Publishable.resource_type html_resource",
    ca = u"Recurs HTML",
    es = u"Recurso HTML",
    en = u"HTML resource"
)

translations.define("woost.models.Publishable.resource_type other",
    ca = u"Altre",
    es = u"Otro",
    en = u"Other"
)

translations.define("Publishable.mime_type",
    ca = u"Tipus MIME",
    es = u"Tipo MIME",
    en = u"MIME type"
)

translations.define("Publishable.per_language_publication",
    ca = u"Publicació per idiomes",
    es = u"Publicación por idiomas",
    en = u"Per language publication"
)

translations.define("Publishable.enabled",
    ca = u"Actiu",
    es = u"Activo",
    en = u"Enabled"
)

translations.define("Publishable.enabled_translations",
    ca = u"Traduccions actives",
    es = u"Traducciones activas",
    en = u"Enabled translations"
)

translations.define("Publishable.websites",
    ca = u"Webs on es publica",
    es = u"Webs donde se publica",
    en = u"Websites where it is published"
)

translations.define("Publishable.websites-explanation",
    ca = u"Webs des de les que es podrà veure i accedir a l'element. Deixar "
         u"en blanc per permetre que l'element aparegui a totes les webs.",
    es = u"Webs des de las que se podrá ver y acceder al elemento. Dejar en "
         u"blanco para permitir que el elemento aparezca en todas las webs.",
    en = u"Websites where the element will be published. Leave blank to share "
         u"this element across all websites."
)

translations.define("Publishable.access_level",
    ca = u"Nivell d'accés",
    es = u"Nivel de acceso",
    en = u"Access level"
)

translations.define("Publishable.access_level=none",
    ca = u"Sense restricció",
    es = u"Sin restricción",
    en = u"No restrictions"
)

translations.define("Publishable.hidden",
    ca = u"Ocult",
    es = u"Oculto",
    en = u"Hidden"
)

translations.define("Publishable.start_date",
    ca = u"Data de publicació",
    es = u"Fecha de publicación",
    en = u"Publication date"
)

translations.define("Publishable.end_date",
    ca = u"Data de caducitat",
    es = u"Fecha de caducidad",
    en = u"Expiration date"
)

translations.define("Publishable.requires_https",
    ca = u"Requereix HTTPS",
    es = u"Requiere HTTPS",
    en = u"Requires HTTPS"
)

translations.define("Publishable.requires_https-explanation",
    ca = u"Aquesta opció només tindrà efecte si la <em>Política "
         u"d'HTTPS</em> del lloc web s'estableix a <em>Decidir a cada "
         u"pàgina</em>.",
    es = u"Esta opción solo tendrá efecto si la <em>Política "
         u"de HTTPS</em> del sitio web se establece a <em>Decidir en cada "
         u"página</em>.",
    en = u"This option will only be taken into account if the site's "
         u"<em>HTTPS policy</em> is set to <em>Decide on a per-page "
         u"basis</em>."
)

translations.define("Publishable.controller",
    ca = u"Controlador",
    es = u"Controlador",
    en = u"Controller"
)

translations.define("Publishable.parent",
    ca = u"Pare",
    es = u"Padre",
    en = u"Parent"
)

translations.define("Publishable.path",
    ca = u"Ruta",
    es = u"Ruta",
    en = u"Path"
)

translations.define("Publishable.full_path",
    ca = u"Ruta completa",
    es = u"Ruta completa",
    en = u"Full path"
)

translations.define("Publishable.caching_policies",
    ca = u"Polítiques de cache",
    es = u"Políticas de cache",
    en = u"Caching policies"
)

translations.define("Publishable.caching_policy-explanation",
    ca = u"Permet establir una política de cache específica per a "
         u"l'element. Si es deixa en blanc s'utilitzarà la política general "
         u"del lloc web.",
    es = u"Permite establecer una política de cache específica para el "
         u"elemento. Si se deja en blanco se utilizará la política general "
         u"del sitio web.",
    en = u"Sets a specific caching policy for this item. Leave blank to fall "
         u"back to the site wide caching policy."
)

translations.define("Publishable.login_page",
    ca = u"Pàgina d'autorització",
    es = u"Página de autorización",
    en = u"Authorization page"
)

translations.define("Publishable.login_page-explanation",
    ca = u"Permet dotar l'element i les seves pàgines filles d'una pàgina "
         u"d'autenticació pròpia. Deixar buit per utilitzar el mateix "
         u"formulari que la resta del lloc web.",
    es = u"Permite dotar al elemento y a sus páginas hijas de una página "
         u"de autenticación propia. Dejar vacío para utilizar el mismo "
         u"formulario que el resto del sitio.",
    en = u"If set, indicates an alternative authentication page to use when "
         u"restricting access to this element or its descending pages. Leave "
         u"blank to use the same authentication form as the rest of the site."
)

# Page
#------------------------------------------------------------------------------
translations.define("Document",
    ca = u"Document",
    es = u"Documento",
    en = u"Document"
)

translations.define("Document-plural",
    ca = u"Documents",
    es = u"Documentos",
    en = u"Documents"
)

translations.define("Document-menu",
    ca = u"Tots els documents",
    es = u"Todos los documentos",
    en = u"All documents"
)

translations.define("Document.content",
    ca = u"Contingut",
    es = u"Contenido",
    en = u"Content"
)

translations.define("Document.meta.robots",
    ca = u"Robots",
    es = u"Robots",
    en = u"Robots"
)

translations.define("Document.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("Document.inner_title",
    ca = u"Títol interior",
    es = u"Título interior",
    en = u"Inner title"
)

translations.define("Document.description",
    ca = u"Descripció",
    es = u"Descripción",
    en = u"Description"
)

translations.define("Document.keywords",
    ca = u"Paraules clau",
    es = u"Palabras clave",
    en = u"Keywords"
)

translations.define("Document.template",
    ca = u"Plantilla",
    es = u"Plantilla",
    en = u"Template"
)

translations.define("Document.children",
    ca = u"Pàgines filles",
    es = u"Páginas hijas",
    en = u"Child pages"
)

translations.define("Document.redirection_mode",
    ca = u"Modalitat de redirecció",
    es = u"Modalidad de redirección",
    en = u"Redirection mode"
)

translations.define("Document.redirection_mode=first_child",
    ca = u"Redirigir al primer fill accessible",
    es = u"Redirigir al primer hijo accesible",
    en = u"Redirect to the first accessible child"
)

translations.define("Document.redirection_mode=custom_target",
    ca = u"Redirigir a un element concret",
    es = u"Redirigir a un elemento concreto",
    en = u"Redirect to a custom target"
)

translations.define("Document.redirection_target",
    ca = u"Destí de la redirecció",
    es = u"Destino de la redirección",
    en = u"Redirection target"
)

translations.define("Document.redirection_method",
    ca = u"Mètode de redirecció",
    es = u"Método de redirección",
    en = u"Redirection method"
)

translations.define("Document.redirection_method=temp",
    ca = u"Temporal",
    es = u"Temporal",
    en = u"Temporary"
)

translations.define("Document.redirection_method=perm",
    ca = u"Permanent",
    es = u"Permanente",
    en = u"Permanent"
)

translations.define("Document.redirection_method=client",
    ca = u"Client",
    es = u"Cliente",
    en = u"Client"
)

translations.define("Document.robots_should_index",
    ca = u"Contingut indexable",
    es = u"Contenido indexable",
    en = u"Indexable content"
)

translations.define("Document.robots_should_follow",
    ca = u"Seguir els enllaços",
    es = u"Seguir los enlaces",
    en = u"Follow links"
)

# DocumentController
#------------------------------------------------------------------------------
translations.define("woost.controllers.DocumentController.redirection_title",
    ca = u"Redirigint",
    es = u"Redirigiendo",
    en = u"Redirecting"
)

translations.define(
    "woost.controllers.DocumentController.redirection_explanation",
    ca = lambda uri:
        u"Redirigint a la pàgina seleccionada. Si no s'obre, fes clic "
        u"<a id='woost-client-redirection' href='%s'>aquí</a>." % uri,
    es = lambda uri:
        u"Redirigiendo a la página seleccionada. Si no se abre, haz clic "
        u"<a id='woost-client-redirection' href='%s'>aquí</a>." % uri,
    en = lambda uri:
        u"Redirecting to the selected page. If it doesn't load, click "
        u"<a id='woost-client-redirection' href='%s'>here</a>." % uri
)

# Redirection
#------------------------------------------------------------------------------
translations.define("Redirection",
    ca = u"Redirecció",
    es = u"Redirección",
    en = u"Redirection"
)

translations.define("Redirection-plural",
    ca = u"Redireccions",
    es = u"Redirecciones",
    en = u"Redirections"
)

translations.define("Redirection.uri",
    ca = u"URL",
    es = u"URL",
    en = u"URL"
)

# Page
#------------------------------------------------------------------------------
translations.define("Page",
    ca = u"Pàgina",
    es = u"Página",
    en = u"Page"
)

translations.define("Page-plural",
    ca = u"Pàgines",
    es = u"Páginas",
    en = u"Pages"
)

translations.define("Page-none",
    es = u"Ninguna"
)

translations.define("Page.blocks",
    ca = u"Cos",
    es = u"Cuerpo",
    en = u"Body"
)

# User
#------------------------------------------------------------------------------
translations.define("User",
    ca = u"Usuari",
    es = u"Usuario",
    en = u"User"
)

translations.define("User-plural",
    ca = u"Usuaris",
    es = u"Usuarios",
    en = u"Users"
)

translations.define("User.email",
    ca = u"Correu electrònic",
    es = u"Correo electrónico",
    en = u"E-mail address",
    pt = u"Email"
)

translations.define("User.password",
    ca = u"Contrasenya",
    es = u"Contraseña",
    en = u"Password",
    pt = u"Palavra-passe",
)

translations.define("User.prefered_language",
    ca = u"Idioma del gestor de continguts",
    es = u"Idioma del gestor de contenidos",
    en = u"Back office language"
)

translations.define("User.backoffice_language_chain",
    ca = u"Idiomes a utilitzar en descriure el contingut",
    es = u"Idiomas a utilizar al describir el contenido",
    en = u"Languages to use when describing content"
)

translations.define("User.backoffice_visible_translations",
    ca = u"Idiomes sempre visibles en editar",
    es = u"Idiomas siempre visibles al editar",
    en = u"Always-on translations"
)

translations.define("User.authored_items",
    ca = u"Contingut creat per l'usuari",
    es = u"Contingut creado por el usuario",
    en = u"Content created by the user"
)

translations.define("User.roles",
    ca = u"Rols",
    es = u"Roles",
    en = u"Roles"
)

translations.define("User.enabled",
    ca = u"Activat",
    es = u"Activado",
    en = u"Enabled"
)

# Permission
#------------------------------------------------------------------------------
translations.define("Permission",
    ca = u"Permís",
    es = u"Permiso",
    en = u"Permission"
)

translations.define("Permission-plural",
    ca = u"Permisos",
    es = u"Permisos",
    en = u"Permissions"
)

translations.define("Permission.role",
    ca = u"Rol",
    es = u"Rol",
    en = u"Role"
)

translations.define("Permission.authorized",
    ca = u"Autoritzat",
    es = u"Autorizado",
    en = u"Authorized"
)

translations.define("Permission.authorized-explanation",
    ca = u"Si es desmarca, el permís passa a actuar com una prohibició",
    es = u"Si se desmarca, el permiso pasa a actuar como una prohibición",
    en = u"If unchecked, the permission is treated as a prohibition"
)

def permission_translation_factory(language, predicate):

    def translate_permission(instance, **kwargs):
        return translations(
            "woost.models.permission",
            language,
            authorized = instance.authorized,
            predicate = predicate(instance, **kwargs)
        )

    return translate_permission

def content_permission_translation_factory(language, predicate):

    def predicate_factory(instance, **kwargs):

        subject = instance.get("subject_description", language)

        if not subject:
            if instance.content_type is None:
                subject = u"?"
            else:
                try:
                    query = instance.select_items()
                except:
                    subject = (
                        decapitalize(
                            translations(
                                instance.content_type.name + "-plural"
                            )
                        )
                        + " "
                        + translations(
                            "woost.models.ContentPermission"
                            "-content_expression_error",
                            language
                        )
                    )
                else:
                    subject = decapitalize(translations(query, language))

        if hasattr(predicate, "__call__"):
            return predicate(instance, subject, **kwargs)
        else:
            return predicate % subject

    return permission_translation_factory(
        language,
        predicate_factory
    )

translations.define(
    "woost.models.ContentPermission-content_expression_error",
    ca = u"(expressió de filtrat incorrecta)",
    es = u"(expresión de filtrado incorrecta)",
    en = u"(incorrect filter)"
)

MEMBER_PERMISSION_ABBR_THRESHOLD = 4

def member_permission_translation_factory(
    language,
    predicate,
    enum,
    abbr,
    any_predicate
):
    def predicate_factory(instance, **kwargs):

        members = list(instance.iter_matching_members(ignore_invalid = True))

        if not members:
            target = any_predicate

        elif len(members) >= MEMBER_PERMISSION_ABBR_THRESHOLD:
            counter = OrderedDict()

            for member in members:
                counter[member.schema] = counter.get(member.schema, 0) + 1

            target = u", ".join(
                abbr(count, content_type)
                for content_type, count in counter.iteritems()
            )
        else:
            subject = u", ".join(
                translations(member, language, qualified = True)
                for member in members
            )

            if hasattr(enum, "__call__"):
                target = enum(instance, subject, **kwargs)
            else:
                target = enum % subject

        return predicate % target

    return permission_translation_factory(
        language,
        predicate_factory
    )

def language_permission_translation_factory(language, predicate, any_predicate):

    def predicate_factory(instance, **kwargs):

        if not instance.matching_languages:
            return any_predicate

        subject = u", ".join(
            translations(perm_lang, language)
            for perm_lang in instance.matching_languages
        )

        if hasattr(predicate, "__call__"):
            return predicate(instance, subject, **kwargs)
        else:
            return predicate % subject

    return permission_translation_factory(
        language,
        predicate_factory
    )

translations.define("woost.models.permission",
    ca = lambda authorized, predicate:
        u"Permís per " + predicate
        if authorized
        else u"Prohibició " + ca_possessive(predicate),
    es = lambda authorized, predicate:
        (u"Permiso para " if authorized else u"Prohibición de ") + predicate,
    en = lambda authorized, predicate:
        (u"Permission to " if authorized else u"Prohibition to ") + predicate,
)

translations.define(
    "woost.models.permission.ReadPermission-instance",
    ca = content_permission_translation_factory("ca", u"llegir %s"),
    es = content_permission_translation_factory("es", u"leer %s"),
    en = content_permission_translation_factory("en", u"read %s")
)

translations.define(
    "woost.models.permission.CreatePermission-instance",
    ca = content_permission_translation_factory("ca", u"crear %s"),
    es = content_permission_translation_factory("es", u"crear %s"),
    en = content_permission_translation_factory("en", u"create %s")
)

translations.define(
    "woost.models.permission.ModifyPermission-instance",
    ca = content_permission_translation_factory("ca", u"modificar %s"),
    es = content_permission_translation_factory("es", u"modificar %s"),
    en = content_permission_translation_factory("en", u"modify %s")
)

translations.define(
    "woost.models.permission.DeletePermission-instance",
    ca = content_permission_translation_factory("ca", u"eliminar %s"),
    es = content_permission_translation_factory("es", u"eliminar %s"),
    en = content_permission_translation_factory("en", u"delete %s")
)

translations.define(
    "woost.models.permission.RenderPermission-instance",
    ca = content_permission_translation_factory(
        "ca",
        lambda permission, subject, **kwargs:
            u"generar imatges " + ca_possessive(subject)
    ),
    es = content_permission_translation_factory(
        "es",
        u"generar imágenes de %s"
    ),
    en = content_permission_translation_factory("en", u"render %s")
)

translations.define(
    "woost.models.permission.ReadMemberPermission-instance",
    ca = member_permission_translation_factory("ca",
        u"llegir %s",
        lambda instance, subject, **kwargs:
            plural2(
                len(instance.matching_members),
                u"el membre %s",
                u"els membres %s"
            ) % subject,
        lambda count, content_type, **kwargs:
            plural2(count, u"1 membre ", u"%d membres " % count)
            + ca_possessive(translations(content_type.name)),
        u"qualsevol membre"
    ),
    es = member_permission_translation_factory("es",
        u"leer %s",
        lambda instance, subject, **kwargs:
            plural2(
                len(instance.matching_members),
                u"el miembro %s",
                u"los miembros %s"
            ) % subject,
        lambda count, content_type, **kwargs:
            plural2(count, u"1 miembro", u"%d miembros" % count)
            + u" de " + (translations(content_type.name)),
        u"cualquier miembro"
    ),
    en = member_permission_translation_factory("en",
        u"read %s",
        lambda instance, subject, **kwargs:
            plural2(
                len(instance.matching_members),
                u"the %s member",
                u"the %s members"
            ) % subject,
        lambda count, content_type, **kwargs:
            plural2(count, u"1 member", u"%d members" % count)
            + u" of " + (translations(content_type.name)),
        u"any member"
    )
)

translations.define(
    "woost.models.permission.ModifyMemberPermission-instance",
    ca = member_permission_translation_factory("ca",
        u"modificar %s",
        lambda instance, subject, **kwargs:
            plural2(
                len(instance.matching_members),
                u"el membre %s",
                u"els membres %s"
            ) % subject,
        lambda count, content_type, **kwargs:
            plural2(count, u"1 membre ", u"%d membres " % count)
            + ca_possessive(translations(content_type.name)),
        u"qualsevol membre"
    ),
    es = member_permission_translation_factory("es",
        u"modificar %s",
        lambda instance, subject, **kwargs:
            plural2(
                len(instance.matching_members),
                u"el miembro %s",
                u"los miembros %s"
            ) % subject,
        lambda count, content_type, **kwargs:
            plural2(count, u"1 miembro", u"%d miembros" % count)
            + u" de " + (translations(content_type.name)),
        u"cualquier miembro"
    ),
    en = member_permission_translation_factory("en",
        u"modify %s",
        lambda instance, subject, **kwargs:
            plural2(
                len(instance.matching_members),
                u"the %s member",
                u"the %s members"
            ) % subject,
        lambda count, content_type, **kwargs:
            plural2(count, u"1 member", u"%d members" % count)
            + u" of " + (translations(content_type.name)),
        u"any member"
    )
)

translations.define(
    "woost.models.permission.ReadTranslationPermission-instance",
    ca = language_permission_translation_factory("ca",
        u"llegir traduccions: %s", u"llegir qualsevol traducció"
    ),
    es = language_permission_translation_factory("es",
        u"leer traducciones: %s", u"leer cualquier traducción"
    ),
    en = language_permission_translation_factory("en",
        u"read translations: %s", u"read any translation"
    )
)

translations.define(
    "woost.models.permission.CreateTranslationPermission-instance",
    ca = language_permission_translation_factory("ca",
        u"crear traduccions: %s", u"crear qualsevol traducció"
    ),
    es = language_permission_translation_factory("es",
        u"crear traducciones: %s", u"crear cualquier traducción"
    ),
    en = language_permission_translation_factory("en",
        u"create translations: %s", u"create any translation"
    )
)

translations.define(
    "woost.models.permission.ModifyTranslationPermission-instance",
    ca = language_permission_translation_factory("ca",
        u"modificar traduccions: %s", u"modificar qualsevol traducció"
    ),
    es = language_permission_translation_factory("es",
        u"modificar traducciones: %s", u"modificar cualquier traducción"
    ),
    en = language_permission_translation_factory("en",
        u"modify translations: %s", u"modify any translation"
    )
)

translations.define(
    "woost.models.permission.DeleteTranslationPermission-instance",
    ca = language_permission_translation_factory("ca",
        u"eliminar traduccions: %s", u"eliminar qualsevol traducció"
    ),
    es = language_permission_translation_factory("es",
        u"eliminar traducciones: %s", u"eliminar cualquier traducción"
    ),
    en = language_permission_translation_factory("en",
        u"delete translations: %s", u"delete any translation"
    )
)

# ContentPermission
#------------------------------------------------------------------------------
translations.define("ContentPermission",
    ca = u"Permís de contingut",
    es = u"Permiso de contenido",
    en = u"Content permission"
)

translations.define("ContentPermission-plural",
    ca = u"Permisos de contingut",
    es = u"Permisos de contenido",
    en = u"Content permissions"
)

translations.define("ContentPermission.content_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Content type"
)

translations.define("ContentPermission.content_expression",
    ca = u"Expressió de filtrat",
    es = u"Expresión de filtrado",
    en = u"Filtering expression"
)

translations.define("ContentPermission.subject_description",
    ca = u"Descripció de l'àmbit del permís",
    es = u"Descripción del ámbito del permiso",
    en = u"Permission scope description"
)

translations.define("ContentPermission.subject_description-explanation",
    ca = u"Permet explicar els elements que es veuran afectats per aquest "
         u"permís. Deixar en blanc per utilitzar una descripció automàtica, "
         u"basada en el tipus i expressió de filtrats seleccionats.",
    es = u"Permite explicar los elementos que se verán afectados por este "
         u"permiso. Dejar en blanco para utilizar una descripción automática "
         u"basada en el tipo y expresión de filtrado seleccionados.",
    en = u"Describes the elements that should be afected by the permission. "
         u"Leave blank to use an automatically generated description, based "
         u"on the selected content type and filters."
)

# ReadPermission
#------------------------------------------------------------------------------
translations.define("ReadPermission",
    ca = u"Permís de lectura",
    es = u"Permiso de lectura",
    en = u"Read content permission"
)

translations.define("ReadPermission-plural",
    ca = u"Permisos de lectura",
    es = u"Permisos de lectura",
    en = u"Read content permissions"
)

# CreatePermission
#------------------------------------------------------------------------------
translations.define("CreatePermission",
    ca = u"Permís de creació",
    es = u"Permiso de creación",
    en = u"Create content permission"
)

translations.define("CreatePermission-plural",
    ca = u"Permisos de creació",
    es = u"Permisos de creación",
    en = u"Create content permissions"
)

# ModifyPermission
#------------------------------------------------------------------------------
translations.define("ModifyPermission",
    ca = u"Permís de modificació",
    es = u"Permiso de modificación",
    en = u"Modify content permission"
)

translations.define("ModifyPermission-plural",
    ca = u"Permisos de modificació",
    es = u"Permisos de modificación",
    en = u"Modify content permissions"
)

# DeletePermission
#------------------------------------------------------------------------------
translations.define("DeletePermission",
    ca = u"Permís d'eliminació",
    es = u"Permiso de eliminación",
    en = u"Delete content permission"
)

translations.define("DeletePermission-plural",
    ca = u"Permisos d'eliminació",
    es = u"Permisos de eliminación",
    en = u"Delete content permissions"
)

# RenderPermission
#------------------------------------------------------------------------------
translations.define("RenderPermission",
    ca = u"Permís de visualització d'imatges",
    es = u"Permiso de visualización de imágenes",
    en = u"Render permission"
)

translations.define("RenderPermission-plural",
    ca = u"Permisos de visualització d'imatges",
    es = u"Permisos de visualización de imágenes",
    en = u"Render permissions"
)

translations.define("RenderPermission.image_factories",
    ca = u"Processat",
    es = u"Procesado",
    en = u"Processing"
)

translations.define("RenderPermission.image_factories-explanation",
    ca = u"Limita el permís o prohibició a un subconjunt de les diferents "
         u"visualitzacions suportades pel lloc web.",
    es = u"Limita el permiso o prohibición a un subconjunto de las distintas "
         u"visualizaciones soportadas por el sitio web.",
    en = u"Limits the permission to a specific subset of the different "
         u"renderings supported by the site."
)

# MemberPermission
#------------------------------------------------------------------------------
translations.define("MemberPermission",
    ca = u"Permís de membre",
    es = u"Permiso de miembro",
    en = u"Member permission"
)

translations.define("MemberPermission-plural",
    ca = u"Permisos sobre els membres",
    es = u"Permisos sobre los miembros",
    en = u"Member permissions"
)

translations.define("MemberPermission.matching_members",
    ca = u"Membres inclosos",
    es = u"Miembros incluidos",
    en = u"Included members"
)

# ReadMemberPermission
#------------------------------------------------------------------------------
translations.define("ReadMemberPermission",
    ca = u"Permís de lectura de membres",
    es = u"Permiso de lectura de miembros",
    en = u"Read members permission"
)

translations.define("ReadMemberPermission-plural",
    ca = u"Permisos de lectura de membres",
    es = u"Permisos de lectura de miembros",
    en = u"Read members permissions"
)

# ModifyMemberPermission
#------------------------------------------------------------------------------
translations.define("ModifyMemberPermission",
    ca = u"Permís de modificació de membres",
    es = u"Permiso de modificación de miembros",
    en = u"Modify members permission"
)

translations.define("ModifyMemberPermission-plural",
    ca = u"Permisos de lectura de membres",
    es = u"Permisos de lectura de miembros",
    en = u"Read members permissions"
)

# TranslationPermission
#------------------------------------------------------------------------------
translations.define("TranslationPermission",
    ca = u"Permís de traducció",
    es = u"Permiso de traducción",
    en = u"Translation permission"
)

translations.define("TranslationPermission-plural",
    ca = u"Permisos de traducció",
    es = u"Permisos de traducción",
    en = u"Translation permissions"
)

translations.define("TranslationPermission.matching_languages",
    ca = u"Idiomes inclosos",
    es = u"Idiomas incluidos",
    en = u"Included languages"
)

# ReadTranslationPermission
#------------------------------------------------------------------------------
translations.define("ReadTranslationPermission",
    ca = u"Permís de lectura de traducció",
    es = u"Permiso de lectura de traducción",
    en = u"Read translation permission"
)

translations.define("ReadTranslationPermission-plural",
    ca = u"Permisos de lectura de traducció",
    es = u"Permisos de lectura de traducción",
    en = u"Read translation permissions"
)

# CreateTranslationPermission
#------------------------------------------------------------------------------
translations.define("CreateTranslationPermission",
    ca = u"Permís de creació de traducció",
    es = u"Permiso de creación de traducción",
    en = u"Create translation permission"
)

translations.define("CreateTranslationPermission-plural",
    ca = u"Permisos de creació de traducció",
    es = u"Permisos de creación de traducción",
    en = u"Create translation permissions"
)

# ModifyTranslationPermission
#------------------------------------------------------------------------------
translations.define("ModifyTranslationPermission",
    ca = u"Permís de modificació de traducció",
    es = u"Permiso de modificación de traducción",
    en = u"Modify translation permission"
)

translations.define("ModifyTranslationPermission-plural",
    ca = u"Permisos de modificació de traducció",
    es = u"Permisos de modificación de traducción",
    en = u"Modify translation permissions"
)

# DeleteTranslationPermission
#------------------------------------------------------------------------------
translations.define("DeleteTranslationPermission",
    ca = u"Permís d'eliminació de traducció",
    es = u"Permiso de eliminación de traducción",
    en = u"Delete translation permission"
)

translations.define("DeleteTranslationPermission-plural",
    ca = u"Permisos d'eliminació de traducció",
    es = u"Permisos de eliminación de traducción",
    en = u"Delete translation permissions"
)

# ReadHistoryPermission
#------------------------------------------------------------------------------
translations.define("ReadHistoryPermission",
    ca = u"Permís de lectura d'històric",
    es = u"Permiso de lectura de histórico",
    en = u"Read past revisions permission"
)

translations.define("ReadMemberPermission-plural",
    ca = u"Permisos de lectura d'històric",
    es = u"Permisos de lectura de histórico",
    en = u"Read past revisions permissions"
)

# InstallationSyncPermission
#------------------------------------------------------------------------------
translations.define("InstallationSyncPermission",
    ca = u"Permís de sincronització",
    es = u"Permiso de sincronización",
    en = u"Synchronization permission"
)

# URI
#------------------------------------------------------------------------------
translations.define("URI",
    ca = u"Adreça web",
    es = u"Dirección web",
    en = u"Web address"
)

translations.define("URI-plural",
    ca = u"Adreces web",
    es = u"Direcciones web",
    en = u"Web addresses"
)

translations.define("URI.content",
    ca = u"Contingut",
    es = u"Contenido",
    en = u"Content"
)

translations.define("URI.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("URI.uri",
    ca = u"Adreça",
    es = u"Dirección",
    en = u"Address"
)

translations.define("URI.language_specific_uri",
    ca = u"Adreça per idioma",
    es = u"Dirección por idioma",
    en = u"Language specific address"
)

translations.define("URI.image",
    ca = u"Imatge",
    es = u"Imagen",
    en = u"Image"
)

# Style
#------------------------------------------------------------------------------
translations.define("Style",
    ca = u"Estil",
    es = u"Estilo",
    en = u"Style"
)

translations.define("Style-plural",
    ca = u"Estils",
    es = u"Estilos",
    en = u"Styles"
)

translations.define("Style.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("Style.custom_class_name",
    ca = u"Classe CSS",
    es = u"Clase CSS",
    en = u"CSS class"
)

translations.define("Style.applicable_to_text",
    ca = u"Aplicable al text",
    es = u"Aplicable al texto",
    en = u"Applies to text"
)

translations.define("Style.applicable_to_blocks",
    ca = u"Aplicable a blocs",
    es = u"Aplicable a bloques",
    en = u"Applicable to blocks"
)

translations.define("Style.custom_class_name-explanation",
    ca = u"Permet especificar el nom de la classe CSS resultant. Si no "
         u"s'indica, el sistema decidirà el nom seguint un patró "
         u"incremental.",
    es = u"Permite especificar el nombre de la clase CSS resultante. Si no "
         u"se indica, el sistema decidirá el nombre siguiendo un patrón "
         u"incremental.",
    en = u"Specifies the name of the resulting CSS class. If no name is "
         u"given, the system will choose a name following an incremental "
         u"pattern."
)

translations.define("Style.declarations",
    ca = u"Declaracions CSS",
    es = u"Declaraciones CSS",
    en = u"CSS declarations"
)

translations.define("Style.admin_declarations",
    ca = u"Declaracions CSS per l'administració",
    es = u"Declaraciones CSS para el administrador",
    en = u"Admin CSS declarations"
)

# UserView
#------------------------------------------------------------------------------
translations.define("UserView",
    ca = u"Vista d'usuari",
    es = u"Vista de usuario",
    en = u"User view"
)

translations.define("UserView-plural",
    ca = u"Vistes d'usuari",
    es = u"Vistas de usuario",
    en = u"User views"
)

translations.define("UserView.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("UserView.parameters",
    ca = u"Vista",
    es = u"Vista",
    en = u"View"
)

translations.define("UserView.roles",
    ca = u"Rols",
    es = u"Roles",
    en = u"Roles"
)

# Back office
#------------------------------------------------------------------------------
translations.define("BackOffice",
    ca = u"Gestor de continguts",
    es = u"Gestor de contenidos",
    en = u"Content manager"
)

translations.define("BackOffice-plural",
    ca = u"Gestors de continguts",
    es = u"Gestores de contenidos",
    en = u"Content managers"
)

# File
#------------------------------------------------------------------------------
translations.define("File",
    ca = u"Fitxer",
    es = u"Fichero",
    en = u"File"
)

translations.define("File-plural",
    ca = u"Fitxers",
    es = u"Ficheros",
    en = u"Files"
)

translations.define("File.content",
    ca = u"Contingut",
    es = u"Contenido",
    en = u"Content"
)

translations.define("File.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("File.file_name",
    ca = u"Nom del fitxer",
    es = u"Nombre del fichero",
    en = u"File name"
)

translations.define("File.file_hash",
    ca = u"Sumatori del contingut del fitxer",
    es = u"Sumatorio del contenido del fichero",
    en = u"Checksum"
)

translations.define("File.file_size",
    ca = u"Mida del fitxer",
    es = u"Tamaño de fichero",
    en = u"File size"
)

translations.define("File.local_path",
    ca = u"Fitxer local",
    es = u"Fichero local",
    en = u"Local file"
)

translations.define("File.image_effects",
    ca = u"Efectes",
    es = u"Efectos",
    en = u"Effects"
)

translations.define("BackOfficeEditForm.upload",
    ca = u"Càrrega de fitxer",
    es = u"Carga de fichero",
    en = u"File upload"
)

# News
#------------------------------------------------------------------------------
translations.define("News",
    ca = u"Notícia",
    es = u"Noticia",
    en = u"News"
)

translations.define("News-plural",
    ca = u"Notícies",
    es = u"Noticias",
    en = u"News"
)

translations.define("News-none",
    es = u"Ninguna"
)

translations.define("News.news_date",
    ca = u"Data de la notícia",
    es = u"Fecha de la noticia",
    en = u"News date"
)

translations.define("News.image",
    ca = u"Imatge",
    es = u"Imagen",
    en = u"Image"
)

translations.define("News.summary",
    ca = u"Sumari",
    es = u"Sumario",
    en = u"Summary"
)

translations.define("News.blocks",
    ca = u"Cos",
    es = u"Cuerpo",
    en = u"Body"
)

# Event
#------------------------------------------------------------------------------
translations.define("Event",
    ca = u"Esdeveniment",
    es = u"Evento",
    en = u"Event"
)

translations.define("Event-plural",
    ca = u"Esdeveniments",
    es = u"Eventos",
    en = u"Events"
)

translations.define("Event.event_start",
    ca = u"Inici de l'esdeveniment",
    es = u"Inicio del evento",
    en = u"Event start"
)

translations.define("Event.event_end",
    ca = u"Fí de l'esdeveniment",
    es = u"Fin del evento",
    en = u"Event end"
)

translations.define("Event.event_location",
    ca = u"Lloc",
    es = u"Lugar",
    en = u"Place"
)

translations.define("Event.image",
    ca = u"Imatge",
    es = u"Imagen",
    en = u"Image"
)

translations.define("Event.summary",
    ca = u"Sumari",
    es = u"Sumario",
    en = u"Summary"
)

translations.define("Event.blocks",
    ca = u"Cos",
    es = u"Cuerpo",
    en = u"Body"
)

# Role
#------------------------------------------------------------------------------
translations.define("Role",
    ca = u"Rol",
    es = u"Rol",
    en = u"Role"
)

translations.define("Role-plural",
    ca = u"Rols",
    es = u"Roles",
    en = u"Roles"
)

translations.define("Role.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("Role.users",
    ca = u"Usuaris",
    es = u"Usuarios",
    en = u"Users"
)

translations.define("Role.user_views",
    ca = u"Vistes d'usuari",
    es = u"Vistas de usuario",
    en = u"User views"
)

translations.define("Role.permissions",
    ca = u"Permisos",
    es = u"Permisos",
    en = u"Permissions"
)

translations.define("Role.base_roles",
    ca = u"Rols base",
    es = u"Roles base",
    en = u"Base roles"
)

translations.define("Role.child_roles",
    ca = u"Rols derivats",
    es = u"Roles derivados",
    en = u"Derived roles"
)

translations.define("Role.default_content_type",
    ca = u"Tipus per defecte",
    es = u"Tipo por defecto",
    en = u"Default content type"
)

translations.define("Role.hidden_content_types",
    ca = u"Tipus ocults",
    es = u"Tipos ocultos",
    en = u"Hidden content types"
)

translations.define("Role.hidden_content_types-explanation",
    ca = u"Una llista de tipus de contingut que no es mostraran a l'usuari. "
         u"Utilitzat per filtrar les entrades del menú principal del gestor.",
    es = u"Una lista de tipos de contenido que no se mostrarán al usuario. "
         u"Utilizado para filtrar las entradas del menú principal del gestor.",
    en = u"A list of content types that will be hidden from the user. Used to "
         u"filter the visible entries in the main menu for the back office "
         u"interface."
)

translations.define("Role.implicit",
    ca = u"Implícit",
    es = u"Implícito",
    en = u"Implicit"
)

translations.define("Role.access_levels",
    ca = u"Nivells d'accés",
    es = u"Niveles de acceso",
    en = u"Access levels"
)

# AccessLevel
#------------------------------------------------------------------------------
translations.define("AccessLevel",
    ca = u"Nivell d'accés",
    es = u"Nivel de acceso",
    en = u"Acces level"
)

translations.define("AccessLevel-plural",
    ca = u"Nivells d'accés",
    es = u"Niveles de acceso",
    en = u"Access levels"
)

translations.define("AccessLevel.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("AccessLevel.roles_with_access",
    ca = u"Rols amb accés",
    es = u"Roles con acceso",
    en = u"Roles with access"
)

translations.define("AccessLevel.restricted_content",
    ca = u"Contingut restringit",
    es = u"Contenido restringido",
    en = u"Restricted content"
)

translations.define("woost.models.accesslevel.AccessLevel-instance",
    ca = lambda instance, **kwargs:
        u"Només per a " + join([
            decapitalize(translations(role))
            for role in instance.roles_with_access
        ]),
    es = lambda instance, **kwargs:
        u"Solo para " + join([
            decapitalize(translations(role))
            for role in instance.roles_with_access
        ]),
    en = lambda instance, **kwargs:
        u"Only for " + join([
            decapitalize(translations(role))
            for role in instance.roles_with_access
        ])
)

# Template
#------------------------------------------------------------------------------
translations.define("Template",
    ca = u"Plantilla",
    es = u"Plantilla",
    en = u"Template"
)

translations.define("Template-plural",
    ca = u"Plantilles",
    es = u"Plantillas",
    en = u"Templates"
)

translations.define("Template-none",
    es = u"Ninguna"
)

translations.define("Template.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("Template.identifier",
    ca = u"Identificador",
    es = u"Identificador",
    en = u"Identifier"
)

translations.define("Template.documents",
    ca = u"Documents",
    es = u"Documentos",
    en = u"Documents"
)

# Controller
#------------------------------------------------------------------------------
translations.define("Controller",
    ca = u"Controlador",
    es = u"Controlador",
    en = u"Controller"
)

translations.define("Controller-plural",
    ca = u"Controladors",
    es = u"Controladores",
    en = u"Controllers"
)

translations.define("Controller.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("Controller.python_name",
    ca = u"Implementació",
    es = u"Implementación",
    en = u"Implementation"
)

translations.define("Controller.python_name-explanation",
    ca = u"Nom qualificat de la implementació del controlador en Python",
    es = u"Nombre cualificado de la implementación del controlador en Python",
    en = u"Qualified name of the Python implementation for the controller"
)

translations.define("Controller.published_items",
    ca = u"Elements publicats",
    es = u"Elementos publicados",
    en = u"Published elements"
)

# Extension
#------------------------------------------------------------------------------
translations.define("Extension",
    ca = u"Extensió",
    es = u"Extensión",
    en = u"Extension"
)

translations.define("Extension-plural",
    ca = u"Extensions",
    es = u"Extensiones",
    en = u"Extensions"
)

translations.define("Extension.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("Extension.description",
    ca = u"Descripció",
    es = u"Descripción",
    en = u"Description"
)

translations.define("Extension.extension_author",
    ca = u"Autor de l'extensió",
    es = u"Autor de la extensión",
    en = u"Extension author"
)

translations.define("Extension.license",
    ca = u"Llicència",
    es = u"Licencia",
    en = u"License"
)

translations.define("Extension.web_page",
    ca = u"Pàgina web",
    es = u"Página web",
    en = u"Web page"
)

translations.define("Extension.enabled",
    ca = u"Activada",
    es = u"Activada",
    en = u"Enabled"
)

translations.define(
    "woost.controllers.backoffice.ExtensionEditNode "
    "enabled extension needs reloading",
    ca = lambda extension:
        u"L'extensió <strong>%s</strong> s'activarà quan es torni a iniciar "
        u"l'aplicació"
        % translations(extension, "ca"),
    es = lambda extension:
        u"La extensión <strong>%s</strong> se activará cuando se reinicie la "
        u"aplicación"
        % translations(extension, "es"),
    en = lambda extension:
        u"The <strong>%s</strong> will be loaded the next time the "
        u"application starts"
        % translations(extension, "en")
)

translations.define(
    "woost.controllers.backoffice.ExtensionEditNode "
    "disabled extension needs reloading",
    ca = lambda extension:
        u"L'extensió <strong>%s</strong> es desactivarà quan es torni "
        u"a iniciar l'aplicació"
        % translations(extension, "ca"),
    es = lambda extension:
        u"La extensión <strong>%s</strong> se desactivará cuando se reinicie "
        u"la aplicación"
        % translations(extension, "es"),
    en = lambda extension:
        u"The <strong>%s</strong> will be unloaded the next time the "
        u"application restarts"
        % translations(extension, "en")
)

# ChangeSet
#------------------------------------------------------------------------------
translations.define("ChangeSet",
    ca = u"Revisió",
    es = u"Revisión",
    en = u"Revision"
)

translations.define("ChangeSet-plural",
    ca = u"Revisions",
    es = u"Revisiones",
    en = u"Revisions"
)

translations.define("ChangeSet.id",
    ca = u"ID",
    es = u"ID",
    en = u"ID"
)

translations.define("ChangeSet.author",
    ca = u"Autor",
    es = u"Autor",
    en = u"Author"
)

translations.define("ChangeSet.date",
    ca = u"Data",
    es = u"Fecha",
    en = u"Date"
)

translations.define("ChangeSet.changes",
    ca = u"Canvis",
    es = u"Cambios",
    en = u"Changes"
)

# Change
#------------------------------------------------------------------------------
translations.define("Change",
    ca = u"Canvi",
    es = u"Cambio",
    en = u"Change"
)

translations.define("Change-plural",
    ca = u"Canvis",
    es = u"Cambios",
    en = u"Changes"
)

translations.define("Change.id",
    ca = u"ID",
    es = u"ID",
    en = u"ID"
)

translations.define("Change.changeset",
    ca = u"Revisió",
    es = u"Revisión",
    en = u"Revision"
)

translations.define("Change.action",
    ca = u"Acció",
    es = u"Acción",
    en = u"Action"
)

translations.define("Change.action=create",
    ca = u"Creat",
    es = u"Creado",
    en = u"Created"
)

translations.define("Change.action=modify",
    ca = u"Modificat",
    es = u"Modificado",
    en = u"Modified"
)

translations.define("Change.action=delete",
    ca = u"Eliminat",
    es = u"Eliminado",
    en = u"Deleted"
)

translations.define("Change.target",
    ca = u"Element afectat",
    es = u"Elemento afectado",
    en = u"Affected item"
)

translations.define("Change.changed_members",
    ca = u"Membres modificats",
    es = u"Miembros modificados",
    en = u"Modified members"
)

translations.define("Change.item_state",
    ca = u"Estat",
    es = u"Estado",
    en = u"State"
)

translations.define("Change.is_explicit_change",
    ca = u"Canvi iniciat per l'usuari",
    es = u"Cambio iniciado por el usuario",
    en = u"Change initiated by the user"
)

def _translate_woost_models_change_instance_ca(action, target):

    if isinstance(target, int):
        target_desc = "%d elements" % target
        apostrophe = False
    else:
        target_desc = translations(target, "ca")

        if not target_desc:
            return ""

        apostrophe = target_desc[0].lower() in u"haeiouàèéíòóú"
        target_desc = u"<em>" + target_desc + u"</em>"

    if action == "edit":
        action_desc = u"Edició"
    elif action == "create":
        action_desc = u"Creació"
    elif action == "delete":
        action_desc = u"Eliminació"
    else:
        return ""

    return action_desc + (" d'" if apostrophe else " de ") + target_desc

def _translate_woost_models_change_instance_es(action, target):

    if isinstance(target, int):
        target_desc = "%d elementos" % target
    else:
        target_desc = translations(target, "es")

        if not target_desc:
            return ""

        target_desc = u"<em>" + target_desc + u"</em>"

    if action == "edit":
        action_desc = u"Edición"
    elif action == "create":
        action_desc = u"Creación"
    elif action == "delete":
        action_desc = u"Eliminación"
    else:
        return ""

    return action_desc + u" de " + target_desc

def _translate_woost_models_change_instance_en(action, target):

    if isinstance(target, int):
        target_desc = "%d items" % target
    else:
        target_desc = translations(target, "ca")

        if not target_desc:
            return ""

        target_desc = u"<em>" + target_desc + u"</em>"

    if action == "edit":
        action_desc = u"modified"
    elif action == "create":
        action_desc = u"created"
    elif action == "delete":
        action_desc = u"deleted"
    else:
        return ""

    return target_desc + u" " + action_desc

translations.define("woost.models.changesets.Change description",
    ca = _translate_woost_models_change_instance_ca,
    es = _translate_woost_models_change_instance_es,
    en = _translate_woost_models_change_instance_en
)

translations.define("woost create action",
    ca = u"Creació",
    es = u"Creación",
    en = u"Creation"
)

translations.define("woost modify action",
    ca = u"Modificació",
    es = u"Modificación",
    en = u"Modification"
)

translations.define("woost delete action",
    ca = u"Eliminació",
    es = u"Eliminación",
    en = u"Eliminació"
)

translations.define(
    "woost.models.userfilter.ChangeSetHasChangeFilter-instance",
    ca = u"Canvis efectuats",
    es = u"Cambios efectuados",
    en = u"Applied changes"
)

translations.define("ChangeSetHasChangeFilter.target",
    ca = u"Element afectat",
    es = u"Elemento afectado",
    en = u"Target object"
)

translations.define("ChangeSetHasChangeFilter.target_type",
    ca = u"Tipus afectat",
    es = u"Tipo afectado",
    en = u"Target type"
)

translations.define("ChangeSetHasChangeFilter.target_type=none",
    ca = u"Qualsevol tipus",
    es = u"Cualquier tipo",
    en = u"Any type"
)

translations.define("ChangeSetHasChangeFilter.action",
    ca = u"Acció",
    es = u"Acción",
    en = u"Action"
)

translations.define("ChangeSetHasChangeFilter.action=none",
    ca = u"Qualsevol acció",
    es = u"Cualquier acción",
    en = u"Any action"
)

# Trigger
#------------------------------------------------------------------------------
translations.define("Trigger",
    ca = u"Disparador",
    es = u"Disparador",
    en = u"Trigger"
)

translations.define("Trigger-plural",
    ca = u"Disparadors",
    es = u"Disparadores",
    en = u"Triggers"
)

translations.define("Trigger.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("Trigger.execution_point",
    ca = u"Moment d'execució",
    es = u"Momento de ejecución",
    en = u"Execution point"
)

translations.define("Trigger.batch_execution",
    ca = u"Execució agrupada",
    es = u"Ejecución agrupada",
    en = u"Batch execution"
)

translations.define("Trigger.batch_execution-explanation",
    ca = u"Si s'agrupa l'execució, el disparador només s'activarà un cop per "
         u"transacció, independentment de quantes accions d'aquest tipus "
         u"s'hagin realitzat.",
    es = u"Si se agrupa la ejecución, el disparador solo se activará una vez "
         u"por transacción, sin importar cuantas acciones de este tipo "
         u"se hayan realizado.",
    en = u"If checked, the trigger will be activated only once per "
         u"transaction, regardless of how many times its activation "
         u"conditions are met."
)

translations.define("Trigger.matching_roles",
    ca = u"Rols a observar",
    es = u"Roles a observar",
    en = u"Watched roles"
)

translations.define("Trigger.matching_roles-explanation",
    ca = u"Si no es selecciona cap rol, el disparador s'activarà "
         u"independentment de l'usuari que inicii l'acció.",
    es = u"Si no se selecciona ningún rol, el disparador se activará "
         u"independientemente del usuario que inicie la acción.",
    en = u"If no role is checked, the trigger will execute regardless "
         u"of which user started the action."
)

translations.define("Trigger.condition",
    ca = u"Condició",
    es = u"Condición",
    en = u"Condition"
)

translations.define("Trigger.condition-explanation",
    ca = u"Una expressió en python que determina si s'executa o no el "
         u"disparador.",
    es = u"Una expresión en python que determina si se ejecuta o no el "
         u"disparador.",
    en = u"A python expression that enables or disables the execution of "
         u"the trigger depending on its context."
)

translations.define("Trigger.custom_context",
    ca = u"Context",
    es = u"Contexto",
    en = u"Context"
)

translations.define("Trigger.custom_context-explanation",
    ca = u"Un bloc de codi Python que permet personalitzar els paràmetres "
         u"que es passaran al disparador en el moment en que sigui executat.",
    es = u"Un bloque de código Python que permite personalizar los parámetros "
         u"que recibirá el disparador en el momento en que sea ejecutado.",
    en = u"A block of Python code that allows to customize the parameters "
         u"that the trigger will receive when it is finally executed."
)

translations.define("Trigger.responses",
    ca = u"Respostes",
    es = u"Respuestas",
    en = u"Responses"
)

translations.define("woost.models.Trigger.execution_point before",
    ca = u"Immediatament",
    es = u"Inmediatamente",
    en = u"Immediately"
)

translations.define("woost.models.Trigger.execution_point after",
    ca = u"En confirmar la transacció",
    es = u"Tras confirmar la transacción",
    en = u"After committing the transaction"
)

# ContentTrigger
#------------------------------------------------------------------------------
translations.define("ContentTrigger",
    ca = u"Disparador per elements",
    es = u"Disparador para elementos",
    en = u"Content trigger"
)

translations.define("ContentTrigger-plural",
    ca = u"Disparadors per contingut",
    es = u"Disparadores para contenido",
    en = u"Content triggers"
)

translations.define("ContentTrigger.matching_items",
    ca = u"Elements a observar",
    es = u"Elementos a observar",
    en = u"Watched items"
)

# CreateTrigger
#------------------------------------------------------------------------------
translations.define("CreateTrigger",
    ca = u"Disparador de creació",
    es = u"Disparador de creación",
    en = u"Create trigger"
)

translations.define("CreateTrigger-plural",
    ca = u"Disparadors de creació",
    es = u"Disparadores de creación",
    en = u"Create triggers"
)

# InsertTrigger
#------------------------------------------------------------------------------
translations.define("InsertTrigger",
    ca = u"Disparador d'inserció",
    es = u"Disparador de inserción",
    en = u"Insert trigger"
)

translations.define("InsertTrigger-plural",
    ca = u"Disparadors d'inserció",
    es = u"Disparadores de inserción",
    en = u"Insert triggers"
)

# ModifyTrigger
#------------------------------------------------------------------------------
translations.define("ModifyTrigger",
    ca = u"Disparador de modificació",
    es = u"Disparador de modificación",
    en = u"Modify trigger"
)

translations.define("ModifyTrigger-plural",
    ca = u"Disparadors de modificació",
    es = u"Disparadores de modificación",
    en = u"Modify triggers"
)

translations.define("ModifyTrigger.matching_members",
    ca = u"Membres a observar",
    es = u"Miembros a observar",
    en = u"Watched members"
)

translations.define("ModifyTrigger.matching_members-explanation",
    ca = u"Si no es selecciona cap membre, el disparador s'activarà "
         u"sigui quin sigui el membre modificat.",
    es = u"Si no se selecciona ningún miembro, el disparador se activará "
         u"sea cual sea el miembro modificado.",
    en = u"If no member is checked, the trigger will execute regardless "
         u"of which member is modified."
)

translations.define("ModifyTrigger.matching_languages",
    ca = u"Idiomes a observar",
    es = u"Idiomas a observar",
    en = u"Watched languages"
)

translations.define("ModifyTrigger.matching_languages-explanation",
    ca = u"Si no es selecciona cap idioma, el disparador s'activarà "
         u"sigui quin sigui l'idioma dels valors modificats.",
    es = u"Si no se selecciona ningún idioma, el disparador se activará "
         u"independientemente del idioma de los valores modificados.",
    en = u"If no language is checked, the trigger will execute regardless "
         u"of which language modified values are translated into."
)

translations.define("woost.controllers.DeleteController.node_deleted_notice",
    ca = u"L'element que estaves editant ha estat eliminat.",
    es = u"El elemento que estabas editando ha sido eliminado.",
    en = u"The item you were editing has been deleted"
)

# DeleteTrigger
#------------------------------------------------------------------------------
translations.define("DeleteTrigger",
    ca = u"Disparador d'eliminació",
    es = u"Disparador de eliminación",
    en = u"Delete trigger"
)

translations.define("DeleteTrigger-plural",
    ca = u"Disparadors d'eliminació",
    es = u"Disparadores de eliminación",
    en = u"Delete triggers"
)

# TriggerResponse
#------------------------------------------------------------------------------
translations.define("TriggerResponse",
    ca = u"Resposta",
    es = u"Respuesta",
    en = u"Trigger response"
)

translations.define("TriggerResponse-plural",
    ca = u"Respostes",
    es = u"Respuestas",
    en = u"Trigger responses"
)

# CustomTriggerResponse
#------------------------------------------------------------------------------
translations.define("CustomTriggerResponse",
    ca = u"Resposta personalitzada",
    es = u"Respuesta personalizada",
    en = u"Custom response"
)

translations.define("CustomTriggerResponse-plural",
    ca = u"Respostes personalitzades",
    es = u"Respuestas personalizadas",
    en = u"Custom responses"
)

translations.define("CustomTriggerResponse.code",
    ca = u"Codi de resposta",
    es = u"Código de respuesta",
    en = u"Response code"
)

# SendEmailTriggerResponse
#------------------------------------------------------------------------------
translations.define("SendEmailTriggerResponse",
    ca = u"Enviament de correu electrònic",
    es = u"Envío de correo electrónico",
    en = u"Send E-mail"
)

translations.define("SendEmailTriggerResponse-plural",
    ca = u"Enviaments de correu electrònic",
    es = u"Envíos de correo electrónico",
    en = u"Send E-mail"
)

translations.define("SendEmailTriggerResponse.email_template",
    ca = u"Plantilla de correu electrònic",
    es = u"Plantilla de correo electrónico",
    en = u"E-mail template"
)

# EmailTemplate
#------------------------------------------------------------------------------
translations.define("EmailTemplate",
    ca = u"Plantilla de correu electrònic",
    es = u"Plantilla de correo electrónico",
    en = u"E-mail template"
)

translations.define("EmailTemplate-plural",
    ca = u"Plantilles de correu electrònic",
    es = u"Plantillas de correo electrónico",
    en = u"E-mail templates"
)

translations.define("EmailTemplate.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("EmailTemplate.mime_type",
    ca = u"Tipus MIME",
    es = u"Tipo MIME",
    en = u"MIME type"
)

translations.define("EmailTemplate.sender",
    ca = u"Remitent",
    es = u"Remitente",
    en = u"Sender"
)

translations.define("EmailTemplate.receivers",
    ca = u"Destinataris",
    es = u"Destinatarios",
    en = u"Receivers"
)

translations.define("EmailTemplate.bcc",
    ca = u"Còpia oculta",
    es = u"Copia oculta",
    en = u"Blind carbon copy"
)

translations.define("EmailTemplate.template_engine",
    ca = u"Motor de pintat",
    es = u"Motor de pintado",
    en = u"Rendering engine"
)

translations.define("EmailTemplate.subject",
    ca = u"Assumpte",
    es = u"Asunto",
    en = u"Subject"
)

translations.define("EmailTemplate.body",
    ca = u"Cos del missatge",
    es = u"Cuerpo del mensaje",
    en = u"Message body"
)

translations.define("EmailTemplate.initialization_code",
    ca = u"Codi d'inicialització",
    es = u"Código de inicialización",
    en = u"Initialization code"
)

translations.define("EmailTemplate.initialization_code-explanation",
    ca = u"Un bloc de codi Python que permet modificar el context que es "
         u"facilita a la resta de camps durant la construcció del missatge "
         u"(útil per definir variables complexes i valors comuns a diferents "
         u"camps o traduccions).",
    es = u"Un bloque de código Python que permite modificar el contexto que "
         u"se facilita al resto de campos durante la construcción del "
         u"mensaje (útil para definir variables complejas o valores comunes a "
         u"distintos campos o traducciones).",
    en = u"A block of Python code that makes it possible to modify the "
         u"context supplid to the other fields when the message is "
         u"constructed (useful in order to more comfortably define complex "
         u"variables or values that must be shared across fields or "
         u"translations)."
)

translations.define("EmailTemplate.language_expression",
    ca = u"Idioma del missatge",
    es = u"Idioma del mensaje",
    en = u"Message language"
)

translations.define("EmailTemplate.language_expression-explanation",
    ca = u"Deixar en blanc per enviar el missatge en l'idioma que estigui "
         u"actiu en el moment. Si es vol forçar l'idioma en que s'hauria "
         u"d'enviar el missatge es pot especificar una expressió Python "
         u"que produeixi el codi ISO de l'idioma desitjat. Cal tindre present "
         u"que aquesta expressió s'evalua abans que el camp <em>codi "
         u"d'inicialització</em>.",
    es = u"Dejar en blanco para enviar el mensaje en el idioma que esté "
         u"activo en el momento. Si se quiere forzar el idioma en que se "
         u"debería enviar el mensaje se puede especificar una expresión "
         u"Python que produzca el código ISO del idioma deseado. Hay que "
         u"tener presente que esta expresión se evalua antes que el campo "
         u"<em>código de inicialización</em>.",
    en = u"Leave it blank to send the message in the presently active "
         u"language. A Python expression can be used to produce the ISO code "
         u"of the desired language. Note that this expression will be "
         u"evaluated before the <em>initialization code</em> field."
)

translations.define("EmailTemplate.condition",
    ca = u"Condició",
    es = u"Condición",
    en = u"Condition"
)

translations.define("EmailTemplate.condition-explanation",
    ca = u"""
        <p>
            Un bloc de codi Python que permet decidir si el missatge s'hauria
            d'enviar o no, en funció dels paràmetres rebuts. Deixar en blanc per
            fer que el missatge s'enviï sempre.
        </p>
        <details>
            <summary>Detalls</summary>
            <p>
                El bloc hauria de definir una variable booleana
                <em>should_send</em> per decidir si el missatge s'enviarà o no.
                Es tindrà accés a tots els paràmetres passats a l'enviament;
                tanmateix, cal tenir en compte que el bloc s'avalua abans que
                el camp <em>codi d'inicialització</em>.
            </p>
        </details>
        """,
    es = u"""
        <p>
            Un bloque de código Python que permite decidir si el mensasje
            debería enviarse o no, en función de los parámetros recibidos. Dejar
            en blanco para que el mensaje se envíe siempre.
        </p>
        <details>
            <summary>Detalles</summary>
            <p>
                El bloque debería definir una variable booleana
                <em>should_send</em> para decidir si el mensaje se enviará o
                no. Se podrá acceder a todos los parámetros pasados durante
                el envío; sin embargo, es necesario tener en cuenta que el
                bloque se evaluará antes que el campo <em>código de
                inicialización</em>.
            </p>
        </details>
        """,
    en = u"""
        <p>
            A block of Python code that decides wether to send the message or
            not, based on the received parameters. Leave blank if there is no
            situation where the message should not be sent.
        </p>
        <details>
            <summary>Details</summary>
            <p>
                The block should define a boolean <em>should_send</em>
                variable, to indicate if the message should be sent or not. All
                parameters given to the e-mail template will be accessible;
                bear in mind that this field is evaluated before executing the
                contents of the <em>initialization code</em> field.
            </p>
        </details>
        """
)

# Feed
#------------------------------------------------------------------------------
translations.define("Feed",
    ca = u"Canal de sindicació",
    es = u"Canal de sindicación",
    en = u"Syndication feed"
)

translations.define("Feed-plural",
    ca = u"Canals de sindicació",
    es = u"Canales de sindicación",
    en = u"Syndication feeds"
)

translations.define("Feed.feed_items",
    ca = u"Elements llistats",
    es = u"Elementos listados",
    en = u"Listed elements"
)

translations.define("Feed.title",
    ca = u"Títol",
    es = u"Título",
    en = u"Title"
)

translations.define("Feed.ttl",
    ca = u"Temps d'expiració (TTL)",
    es = u"Tiempo de expiración (TTL)",
    en = u"TTL"
)

translations.define("Feed.image",
    ca = u"Imatge",
    es = u"Imagen",
    en = u"Image"
)

translations.define("Feed.description",
    ca = u"Descripció",
    es = u"Descripción",
    en = u"Description"
)

translations.define("Feed.limit",
    ca = u"Límit d'elements publicats",
    es = u"Límite de elementos publicados",
    en = u"Published items limit"
)

translations.define("Feed.query_parameters",
    ca = u"Elements publicats",
    es = u"Elementos publicados",
    en = u"Published items"
)

translations.define("Feed.item_title_expression",
    ca = u"Expressió pel títol dels elements",
    es = u"Expresión para el título de los elementos",
    en = u"Item title expression"
)

translations.define("Feed.item_link_expression",
    ca = u"Expressió per l'enllaç dels elements",
    es = u"Expresión para el enlace de los elementos",
    en = u"Item link expression"
)

translations.define("Feed.item_publication_date_expression",
    ca = u"Expressió per la data de publicació dels elements",
    es = u"Expresión para la fecha de publicación de los elementos",
    en = u"Item publication date expression"
)

translations.define("Feed.item_description_expression",
    ca = u"Expressió per la descripció dels elements",
    es = u"Expresión para la descripción de los elementos",
    en = u"Item description expression"
)

# ContentTypePicker
#------------------------------------------------------------------------------
translations.define("woost.views.ContentTypePicker select",
    ca = u"Seleccionar",
    es = u"Seleccionar",
    en = u"Select"
)

translations.define("woost.views.ContentTypePicker accept",
    ca = u"Acceptar",
    es = u"Aceptar",
    en = u"Accept"
)

translations.define("woost.views.ContentTypePicker cancel",
    ca = u"Cancel·lar",
    es = u"Cancelar",
    en = u"Cancel"
)

translations.define("woost.views.ContentTypePicker.empty_label",
    ca = u"Cap",
    es = u"Ninguno",
    en = u"None"
)

# Preview
#------------------------------------------------------------------------------
translations.define("woost.backoffice invalid item preview",
    ca = u"Algun camp del formulari no té un format correcte. "
         u"No es pot realitzar la vista prèvia.",
    es = u"Algún campo del formulario no tiene un formato correcto. "
         u"No se puede realizar la vista previa.",
    en = u"Some form field has no correct format. "
         u"Impossible to render preview."
)

translations.define(
    "woost.views.BackOfficePreviewView.language_dropdown_label",
    ca = u"Idioma:",
    es = u"Idioma:",
    en = u"Language:"
)

translations.define(
    "woost.views.BackOfficePreviewView.language_dropdown_label.shortcut",
    ca = u"i",
    es = u"i",
    en = u"l"
)

# Expressions
#------------------------------------------------------------------------------
translations.define(
    "woost.models.publishable.IsPublishedExpression-instance",
    ca = u"publicat",
    es = u"publicado",
    en = u"published"
)

translations.define(
    "woost.models.publishable.IsAccessibleExpression-instance",
    ca = u"accessible",
    es = u"accesible",
    en = u"accessible"
)

translations.define(
    "woost.models.publishable.UserHasAccessLevelExpression-instance",
    ca = u"amb nivell d'accés adequat",
    es = u"con nivel de acceso adecuado",
    en = u"with a valid access level"
)

# PasswordChange
#------------------------------------------------------------------------------
translations.define(
    "woost.controllers.passwordchangecontroller.request_sended_notification_message",
    ca = u"""
        <p>
            Hem enviat un correu electrònic a l'adreça indicada amb les
            instruccions per reestablir la contrasenya.
        </p>
        """,
    es = u"""
        <p>
            Hemos enviado un correo electrónico a la dirección indicada con
            las instrucciones para reestablecer tu contraseña.
        </p>
        """,
    en = u"""
        <p>
            We have sent an e-mail message to the indicated account
            containing further instructions to reset your password.
        </p>
        """,
    pt = u"""
        <p>
            Foi enviado um e-mail para o endereço indicado com as instruções
            para redefinir a sua palavra-passe.
        </p>
        """
)

translations.define(
    "woost.controllers.passwordchangecontroller.confirmation_message",
    ca = u"<p>Canvi de contrasenya realitzat correctament.</p>",
    es = u"<p>Cambio de contraseña realizado correctamente.</p>",
    en = u"<p>Password correctly changed.</p>",
    pt = u"<p>Alteração da palavra-passe efetuada corretamente.</p>"
)

translations.define(
    "woost.controllers.passwordchangecontroller."
    "UserIdentifierNotRegisteredError-instance",
    ca = u"No existeix cap usuari amb aquest identificador",
    es = u"No existe ningún usuario registrado con este identificador",
    en = u"There is no user with the indicated identifier",
    pt = u"Não existe nenhum utilizador registado com este nome"
)

translations.define(
    "woost.controllers.passwordchangecontroller."
    "UserEmailMissingError-instance",
    ca = u"L'usuari que has indicat no té cap adreça de correu electrònic "
         u"associada: no es pot canviar la seva contrasenya a través "
         u"d'aquest formulari.",
    es = u"El usuario que has indicado no tiene ninguna dirección de "
         u"correo electrónico asociada: no se puede cambiar su contraseña a "
         u"través de este formulario.",
    en = u"The user you indicated has no known e-mail address. Only users "
         u"with verified e-mail addresses can use this form to change their "
         u"password.",
    pt = u"""O utilizador indicado não tem nenhum endereço de e-mail associado:
    não é possível alterar a sua palavra-passe através deste formulário."""
)

translations.define(
    "PasswordChangeConfirmationForm.password_confirmation",
    ca = u"Confirmar la contrasenya",
    es = u"Confirmar la contraseña",
    en = u"Confirm password",
    pt = u"Confirmar a palavra-passe"
)

# EditPanel
#------------------------------------------------------------------------------
translations.define("woost.views.EditPanel.show_panel_button",
    ca = u"Mostrar panell d'edició",
    es = u"Mostrar panel de edición",
    en = u"Show edit panel"
)

translations.define("woost.views.EditPanel.close_panel_button",
    ca = u"Ocultar panell d'edició",
    es = u"Ocultar panel de edición",
    en = u"Close edit panel"
)

translations.define("woost.views.EditPanel.actions_title",
    ca = u"Accions",
    es = u"Acciones",
    en = u"Actions"
)

# Renderer
#------------------------------------------------------------------------------
translations.define("Renderer",
    ca = u"Pintador d'imatges",
    es = u"Pintador de imágenes",
    en = u"Renderer"
)

translations.define("Renderer-plural",
    ca = u"Pintadors d'imatges",
    es = u"Pintadores de imágenes",
    en = u"Renderers"
)

translations.define("Renderer.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

# ImageFileRenderer
#------------------------------------------------------------------------------
translations.define("ImageFileRenderer",
    ca = u"Pintador de fitxers d'imatge",
    es = u"Pintador de ficheros de imagen",
    en = u"Image file renderer"
)

translations.define("ImageFileRenderer-plural",
    ca = u"Pintadors de fitxers d'imatge",
    es = u"Pintadores de ficheros de imagen",
    en = u"Image file renderers"
)

translations.define("ImageFileRenderer.max_size",
    ca = u"Mida màxima",
    es = u"Tamaño máximo",
    en = u"Max size"
)

translations.define("ImageFileRenderer.max_size-explanation",
    ca = u"Evita que el servidor processi imatges amb una mida excessiva. "
         u"La mida màxima a processar s'ha d'indicar amb dos valors enters, "
         u"separats per un caràcter 'x' (per exemple, 2000 x 1500). Les "
         u"mides es validaran en orientació vertical o horitzontal, "
         u"indistintament.",
    es = u"Evita que el servidor procese imágenes con un tamaño excesivo. "
         u"El tamaño máximo admisible debe indicarse con dos valores "
         u"enteros, separados por un carácter 'x' (por ejemplo, 2000 x "
         u"1500). El tamaño se validará en orientación vertical o "
         u"horizontal, indistintamente.",
    en = u"Prevents the server from processing excessively large images. The "
         u"maximum image size allowed has to be indicated as a tuple of two "
         u"integers, separated by an 'x' character (ie. 2000 x 1500). Images "
         u"will be validated against this size constraint in both landscape "
         u"and portrait orientations."
)

# IconRenderer
#------------------------------------------------------------------------------
translations.define("IconRenderer",
    ca = u"Llibreria d'icones",
    es = u"Librería de iconos",
    en = u"Icon library"
)

translations.define("IconRenderer-plural",
    ca = u"Llibreries de icones",
    es = u"Librerías de iconos",
    en = u"Icon libraries"
)

translations.define("IconRenderer.icon_resolver_expression",
    ca = u"Proveïdor d'icones",
    es = u"Proveedor de iconos",
    en = u"Icon resolver"
)

translations.define("IconRenderer.icon_resolver_expression-explanation",
    ca = u"Referència a una instància de "
         u"<em>woost.iconresolver.IconResolver.</em> Deixar buit per "
         u"utilitzar <em>woost.app.icon_resolver</em>.",
    es = u"Referencia a una instancia de "
         u"<em>woost.iconresolver.IconResolver.</em> Dejar vacío para "
         u"utilizar <em>woost.app.icon_resolver</em>.",
    en = u"Reference to an instance of "
         u"<em>woost.iconresolver.IconResolver.</em> Leave blank to use "
         u"<em>woost.app.icon_resolver</em>."
)

translations.define("IconRenderer.icon_size",
    ca = u"Mida de les icones",
    es = u"Tamaño de los iconos",
    en = u"Icon size"
)

# HTMLRenderer
#------------------------------------------------------------------------------
translations.define("HTMLRenderer",
    ca = u"Pintador de documents HTML",
    es = u"Pintador de documentos HTML",
    en = u"HTML renderer"
)

translations.define("HTMLRenderer-plural",
    ca = u"Pintadors de documents HTML",
    es = u"Pintadores de documentos HTML",
    en = u"HTML renderers"
)

translations.define("HTMLRenderer.window_width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("HTMLRenderer.window_height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

translations.define("HTMLRenderer.external_urls_only",
    ca = u"Només URLs externes",
    es = u"Sólo URLs externals",
    en = u"External URLs only"
)

# ImageURIRenderer
#------------------------------------------------------------------------------
translations.define("ImageURIRenderer",
    ca = u"Pintador d'imatges remotes",
    es = u"Pintador de imágenes remotas",
    en = u"Image URI renderer"
)

translations.define("ImageURIRenderer-plural",
    ca = u"Pintadors d'imatges remotes",
    es = u"Pintadores de imágenes remotas",
    en = u"Image URI renderers"
)

# PDFRenderer
#------------------------------------------------------------------------------
translations.define("PDFRenderer",
    ca = u"Pintador de documents PDF",
    es = u"Pintador de documentos PDF",
    en = u"PDF renderer"
)

translations.define("PDFRenderer-plural",
    ca = u"Pintadors de documents PDF",
    es = u"Pintadores de documentos PDF",
    en = u"PDF renderers"
)

translations.define("PDFRenderer.command",
    ca = u"Comanda",
    es = u"Comando",
    en = u"Command"
)

translations.define("PDFRenderer.timeout",
    ca = u"Temps màxim d'execució",
    es = u"Tiempo máximo de ejecución",
    en = u"Timeout"
)

translations.define("PDFRenderer.timeout_size_factor",
    ca = u"Temps de gràcia segons la mida del fitxer",
    es = u"Tiempo de gracia según el tamaño del fichero",
    en = u"Timeout file size factor"
)

# VideoFileRenderer
#------------------------------------------------------------------------------
translations.define("VideoFileRenderer",
    ca = u"Pintador de fitxers de vídeo",
    es = u"Pintador de ficheros de video",
    en = u"Video file renderer"
)

translations.define("VideoFileRenderer-plural",
    ca = u"Pintadors de fitxers de vídeo",
    es = u"Pintadores de ficheros de video",
    en = u"Video file renderers"
)

# ChainRenderer
#------------------------------------------------------------------------------
translations.define("ChainRenderer",
    ca = u"Pintador en cadena",
    es = u"Pintador en cadena",
    en = u"Chain renderer"
)

translations.define("ChainRenderer-plural",
    ca = u"Pintadors en cadena",
    es = u"Pintadores en cadena",
    en = u"Chain renderers"
)

translations.define("ChainRenderer.renderers",
    ca = u"Pintadors",
    es = u"Pintadores",
    en = u"Renderers"
)

# ImageFactory
#------------------------------------------------------------------------------
translations.define("ImageFactory",
    ca = u"Processador d'imatges",
    es = u"Procesador de imágenes",
    en = u"Image factory"
)

translations.define("ImageFactory-plural",
    ca = u"Processadors d'imatges",
    es = u"Procesadores de imágenes",
    en = u"Image factories"
)

translations.define("ImageFactory.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("ImageFactory.identifier",
    ca = u"Identificador",
    es = u"Identificador",
    en = u"Identifier"
)

translations.define("ImageFactory.identifier-explanation",
    ca = u"Un valor únic que permet accedir al processador programàticament",
    es = u"Un valor único que permite acceder al procesador "
         u"programáticamente",
    en = u"A unique value that makes it possible to access the image factory "
         u"programmatically"
)

translations.define("ImageFactory.renderer",
    ca = u"Pintador",
    es = u"Pintador",
    en = u"Renderer"
)

translations.define("ImageFactory.renderer-explanation",
    ca = u"Especifica la manera en que s'obté la imatge",
    es = u"Especifica la manera en que se obtiene la imagen",
    en = u"Determines the source of produced images"
)

translations.define("ImageFactory.default_format",
    ca = u"Format d'imatge",
    es = u"Formato de imagen",
    en = u"Image format"
)

translations.define("ImageFactory.effects",
    ca = u"Efectes",
    es = u"Efectos",
    en = u"Effects"
)

translations.define("ImageFactory.options_code",
    ca = u"Opcions",
    es = u"Opciones",
    en = u"Options"
)

translations.define("ImageFactory.options_code-explanation",
    ca = u"""
        <p>
            Fragment de codi Python que permet passar paràmetres al mètode save
            de PIL.
        </p>
        <details>
            <summary>Detalls</summary>
            <p>
                Es proporcionen les variables següents:
            </p>
            <dl>
                <dt>options</dt>
                <dd>Diccionari amb els paràmetres que es passaran al mètode save.
                    Documentació:
                    <a href='http://effbot.org/imagingbook/format-jpeg.htm'>
                        JPEG
                    </a>,
                    <a href='http://effbot.org/imagingbook/format-png.htm'>
                        PNG
                    </a>,
                    <a href='http://effbot.org/imagingbook/format-gif.htm'>
                        GIF
                    </a>
                </dd>
                <dt>format</dt>
                <dd>JPEG | PNG | GIF.</dd>
                <dt>factory</dt>
                <dd>El processador d'imatge.</dd>
                <dt>image</dt>
                <dd>Referència a l'element que s'està pintant.</dd>
            </dl>
        </details>
    """,
    es = u"""
        <p>
            Fragmento de código Python que permite pasar parámetros al método
            save de PIL.
        </p>
        <details>
            <summary>Detalles</summary>
            <p>
                Se proporcionan las variables siguientes:
            </p>
            <dl>
                <dt>options</dt>
                <dd>Diccionario con los parámetros que se pasaran al método save.
                    Documentación:
                    <a href='http://effbot.org/imagingbook/format-jpeg.htm'>
                        JPEG
                    </a>,
                    <a href='http://effbot.org/imagingbook/format-png.htm'>
                        PNG
                    </a>,
                    <a href='http://effbot.org/imagingbook/format-gif.htm'>
                        GIF
                    </a>
                </dd>
                <dt>format</dt>
                <dd>JPEG | PNG | GIF.</dd>
                <dt>factory</dt>
                <dd>El procesador de imagen.</dd>
                <dt>image</dt>
                <dd>Referencia al elemento que se está pintando.</dd>
            </dl>
        </details>
    """,
    en = u"""
        <p>
            A Python code snippet to pass parameters to PIL's save method.
        </p>
        <details>
            <summary>Details</summary>
            <p>
                The code snippet will have access to the following variables:
            </p>
            <dl>
                <dt>options</dt>
                <dd>A dictionary containing the parameters to be passed to the save method.
                    Documentation:
                    <a href='http://effbot.org/imagingbook/format-jpeg.htm'>
                        JPEG
                    </a>,
                    <a href='http://effbot.org/imagingbook/format-png.htm'>
                        PNG
                    </a>,
                    <a href='http://effbot.org/imagingbook/format-gif.htm'>
                        GIF
                    </a>
                </dd>
                <dt>format</dt>
                <dd>JPEG | PNG | GIF.</dd>
                <dt>factory</dt>
                <dd>The image processor.</dd>
                <dt>image</dt>
                <dd>A reference to the element.</dd>
            </dl>
        </details>
    """,
)

translations.define("ImageFactory.fallback",
    ca = u"Processador alternatiu",
    es = u"Procesador alternativo",
    en = u"Fallback"
)

translations.define("ImageFactory.fallback-explanation",
    ca = u"Si el processador és incapaç de produïr una imatge, "
         u"es provarà d'obtenir una imatge substitutiva utilitzant "
         u"el processador alternatiu indicat",
    es = u"Si el procesador es incapaz de producir una imagen, se "
         u"intentará obtener una imagen sustitutiva utilizando el "
         u"procesador alternativo indicado",
    en = u"If the image factory fails to produce an image, it will try to "
         u"fall back to the indicated factory to produce an alternative image"
)

translations.define("ImageFactory.applicable_to_blocks",
    ca = u"Aplicable a blocs",
    es = u"Aplicable a bloques",
    en = u"Applicable to blocks"
)

# ImageEffect
#------------------------------------------------------------------------------
translations.define("ImageEffect",
    ca = u"Efecte d'imatge",
    es = u"Efecto de imagen",
    en = u"Image effect"
)

translations.define("ImageEffect-plural",
    ca = u"Efectes d'imatge",
    es = u"Efectos de imagen",
    en = u"Image effects"
)

translations.define(
    "woost.models.rendering.horizontal_alignment=left",
    ca = u"Esquerra",
    es = u"Izquierda",
    en = u"Left"
)

translations.define(
    "woost.models.rendering.horizontal_alignment=center",
    ca = u"Centrat",
    es = u"Centrado",
    en = u"Center"
)

translations.define(
    "woost.models.rendering.horizontal_alignment=right",
    ca = u"Dreta",
    es = u"Derecha",
    en = u"Right"
)

translations.define(
    "woost.models.rendering.vertical_alignment=top",
    ca = u"A dalt",
    es = u"Arriba",
    en = u"Top"
)

translations.define(
    "woost.models.rendering.vertical_alignment=center",
    ca = u"Centrat",
    es = u"Centrado",
    en = u"Center"
)

translations.define(
    "woost.models.rendering.vertical_alignment=bottom",
    ca = u"A baix",
    es = u"Abajo",
    en = u"Bottom"
)

# Thumbnail
#------------------------------------------------------------------------------
translations.define("Thumbnail",
    ca = u"Redimensionar",
    es = u"Redimensionar",
    en = u"Resize"
)

translations.define("Thumbnail-plural",
    ca = u"Efectes de redimensionat",
    es = u"Efectos de redimensionat",
    en = u"Resize effects"
)

translations.define("Thumbnail.width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("Thumbnail.height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

translations.define("Thumbnail.upscale",
    ca = u"Permetre ampliar les imatges",
    es = u"Permitir ampliar las imágenes",
    en = u"Allow image upscaling"
)

# Crop
#------------------------------------------------------------------------------
translations.define("Crop",
    ca = u"Retallar",
    es = u"Recortar",
    en = u"Crop"
)

translations.define("Crop-plural",
    ca = u"Efectes de retallat",
    es = u"Efectos de recorte",
    en = u"Crop effects"
)

translations.define("Crop.left",
    ca = u"X1",
    es = u"X1",
    en = u"X1"
)

translations.define("Crop.top",
    ca = u"Y1",
    es = u"Y1",
    en = u"Y1"
)

translations.define("Crop.right",
    ca = u"X2",
    es = u"X2",
    en = u"X2"
)

translations.define("Crop.bottom",
    ca = u"Y2",
    es = u"Y2",
    en = u"Y2"
)

# AutoCrop
#------------------------------------------------------------------------------
translations.define("AutoCrop",
    ca = u"Retallat automàtic",
    es = u"Recorte automático",
    en = u"Autocrop"
)

translations.define("AutoCrop-plural",
    ca = u"Efectes de retallat automàtic",
    es = u"Efectos de recorte automático",
    en = u"Autocrop effects"
)

# Fill
#------------------------------------------------------------------------------
translations.define("Fill",
    ca = u"Redimensionar i retallar",
    es = u"Redimensionar y recortar",
    en = u"Thumbnail and crop"
)

translations.define("Fill-plural",
    ca = u"Efectes de redimensionar i retallar",
    es = u"Efectos redimensionar y recortar",
    en = u"Thumbnail and crop effects"
)

translations.define("Fill.width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("Fill.height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

translations.define("Fill.upscale",
    ca = u"Permetre ampliar les imatges",
    es = u"Permitir ampliar las imágenes",
    en = u"Allow image upscaling"
)

translations.define("Fill.horizontal_alignment",
    ca = u"Alineament horitzontal",
    es = u"Alineamiento horizontal",
    en = u"Horizontal alignment"
)

translations.define("Fill.vertical_alignment",
    ca = u"Alineament vertical",
    es = u"Alineamiento vertical",
    en = u"Vertical alignment"
)

translations.define("Fill.preserve_vertical_images",
    ca = u"Preservar imatges verticals",
    es = u"Preservar imágenes verticales",
    en = u"Preserve vertical images"
)

# Rotate
#------------------------------------------------------------------------------
translations.define("Rotate",
    ca = u"Rotar",
    es = u"Rotar",
    en = u"Rotate"
)

translations.define("Rotate-plural",
    ca = u"Rotacions",
    es = u"Rotaciones",
    en = u"Rotations"
)

translations.define("Rotate.angle",
    ca = u"Angle",
    es = u"Ángulo",
    en = u"Angle"
)

# Color
#------------------------------------------------------------------------------
translations.define("Color",
    ca = u"Intensitat del color",
    es = u"Intensidad del color",
    en = u"Color intensity"
)

translations.define("Color-plural",
    ca = u"Efectes d'intensitat del color",
    es = u"Efectos de intensidad del color",
    en = u"Color intensity effects"
)

translations.define("Color.level",
    ca = u"Nivell",
    es = u"Nivel",
    en = u"Level"
)

# Brightness
#------------------------------------------------------------------------------
translations.define("Brightness",
    ca = u"Lluminositat",
    es = u"Luminosidad",
    en = u"Brightness"
)

translations.define("Brightness-plural",
    ca = u"Efectes de lluminositat",
    es = u"Efectos de luminosidad",
    en = u"Brightness effects"
)

translations.define("Brightness.level",
    ca = u"Nivell",
    es = u"Nivel",
    en = u"Level"
)

# Contrast
#------------------------------------------------------------------------------
translations.define("Contrast",
    ca = u"Contrast",
    es = u"Contraste",
    en = u"Contrast"
)

translations.define("Contrast-plural",
    ca = u"Efectes de contrast",
    es = u"Efectos de contraste",
    en = u"Contrast effects"
)

translations.define("Contrast.level",
    ca = u"Nivell",
    es = u"Nivel",
    en = u"Level"
)

# Sharpness
#------------------------------------------------------------------------------
translations.define("Sharpness",
    ca = u"Definició",
    es = u"Definición",
    en = u"Sharpness"
)

translations.define("Sharpness-plural",
    ca = u"Efectes de definició",
    es = u"Efectos de definición",
    en = u"Sharpness effects"
)

translations.define("Sharpness.level",
    ca = u"Nivell",
    es = u"Nivel",
    en = u"Level"
)

# Frame
#------------------------------------------------------------------------------
translations.define("Frame",
    ca = u"Marc",
    es = u"Marco",
    en = u"Frame"
)

translations.define("Frame-plural",
    ca = u"Marcs",
    es = u"Marcos",
    en = u"Frames"
)


translations.define("Frame.edge_width",
    ca = u"Gruix del marc",
    es = u"Grueso del marco",
    en = u"Edge width"
)

translations.define("Frame.edge_color",
    ca = u"Color del marc",
    es = u"Color del marco",
    en = u"Edge color"
)

translations.define("Frame.vertical_padding",
    ca = u"Espaiat vertical",
    es = u"Espaciado vertical",
    en = u"Vertical padding"
)

translations.define("Frame.horizontal_padding",
    ca = u"Espaiat horitzontal",
    es = u"Espaciado horizontal",
    en = u"Horizontal padding"
)

translations.define("Frame.background",
    ca = u"Color de fons",
    es = u"Color de fondo",
    en = u"Background"
)

# Shadow
#------------------------------------------------------------------------------
translations.define("Shadow",
    ca = u"Ombra",
    es = u"Sombra",
    en = u"Shadow"
)

translations.define("Shadow-plural",
    ca = u"Ombres",
    es = u"Sombras",
    en = u"Shadows"
)

translations.define("Shadow.offset",
    ca = u"Desplaçament",
    es = u"Desplazamiento",
    en = u"Offset"
)

translations.define("Shadow.padding",
    ca = u"Espaiat",
    es = u"Espaciado",
    en = u"Padding"
)

translations.define("Shadow.color",
    ca = u"Color",
    es = u"Color",
    en = u"Color"
)

# ReducedOpacity
#------------------------------------------------------------------------------
translations.define("ReducedOpacity",
    ca = u"Reduïr l'opacitat",
    es = u"Reducir la opacidad",
    en = u"Reduce opacity"
)

translations.define("ReducedOpacity-plural",
    ca = u"Reduccions d'opacitat",
    es = u"Reducciones de opacidad",
    en = u"Opacity reductions"
)

translations.define("ReducedOpacity.level",
    ca = u"Nivell",
    es = u"Nivel",
    en = u"Level"
)

# Fade
#------------------------------------------------------------------------------
translations.define("Fade",
    ca = u"Esvaïr",
    es = u"Desvanecer",
    en = u"Fade"
)

translations.define("Fade-plural",
    ca = u"Esvaïments",
    es = u"Desvanecimientos",
    en = u"Fade effects"
)

translations.define("Fade.top_width",
    ca = u"Gruix superior",
    es = u"Ancho superior",
    en = u"Top width"
)

translations.define("Fade.right_width",
    ca = u"Gruix a la dreta",
    es = u"Ancho derecho",
    en = u"Right width"
)

translations.define("Fade.bottom_width",
    ca = u"Gruix inferior",
    es = u"Ancho inferior",
    en = u"Bottom width"
)

translations.define("Fade.left_width",
    ca = u"Gruix a l'esquerra",
    es = u"Ancho a la izquierda",
    en = u"Left width"
)

translations.define("Fade.edge_opacity",
    ca = u"Opacitat exterior",
    es = u"Opacidad exterior",
    en = u"Edge opacity"
)

translations.define("Fade.inner_opacity",
    ca = u"Opacitat interior",
    es = u"Opacidad interior",
    en = u"Inner opacity"
)

# Watermark
#------------------------------------------------------------------------------
translations.define("Watermark",
    ca = u"Marca d'aigua",
    es = u"Marca de agua",
    en = u"Watermark"
)

translations.define("Watermark-plural",
    ca = u"Marques d'aigua",
    es = u"Marcas de agua",
    en = u"Watermarks"
)

translations.define("Watermark.mark",
    ca = u"Marca",
    es = u"Marca",
    en = u"Mark"
)

translations.define("Watermark.opacity",
    ca = u"Opacitat",
    es = u"Opacidad",
    en = u"Opacity"
)

translations.define("Watermark.placement",
    ca = u"Posicionament",
    es = u"Posicionamiento",
    en = u"Positioning"
)

translations.define("Watermark.placement=middle",
    ca = u"Centrat",
    es = u"Centrado",
    en = u"In the middle"
)

translations.define("Watermark.placement=scale",
    ca = u"Omplir",
    es = u"Rellenar",
    en = u"Scale"
)

translations.define("Watermark.placement=tile",
    ca = u"Repetir",
    es = u"Repetir",
    en = u"Tile"
)

# Flip
#------------------------------------------------------------------------------
translations.define("Flip",
    ca = u"Capgirar",
    es = u"Voltear",
    en = u"Flip"
)

translations.define("Flip-plural",
    ca = u"Efectes de capgirar",
    es = u"Efectos de volteado",
    en = u"Flip effects"
)

translations.define("Flip.axis",
    ca = u"Eix",
    es = u"Eje",
    en = u"Axis"
)

translations.define("Flip.axis=horizontal",
    ca = u"Horitzontal",
    es = u"Horizontal",
    en = u"Horizontal"
)

translations.define("Flip.axis=vertical",
    ca = u"Vertical",
    es = u"Vertical",
    en = u"Vertical"
)

# Align
#------------------------------------------------------------------------------
translations.define("Align",
    ca = u"Aliniar",
    es = u"Alinear",
    en = u"Align"
)

translations.define("Align-plural",
    ca = u"Alineaments",
    es = u"Alineamientos",
    en = u"Alignments"
)

translations.define("Align.width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("Align.height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

translations.define("Align.horizontal_alignment",
    ca = u"Alineament horitzontal",
    es = u"Alineamiento horizontal",
    en = u"Horizontal alignment"
)

translations.define("Align.vertical_alignment",
    ca = u"Alineament vertical",
    es = u"Alineamiento vertical",
    en = u"Vertical alignment"
)

translations.define("Align.background",
    ca = u"Color de fons",
    es = u"Color de fondo",
    en = u"Background"
)

# Grayscale
#------------------------------------------------------------------------------
translations.define("Grayscale",
    ca = u"Tons de gris",
    es = u"Tonos de gris",
    en = u"Grayscale"
)

translations.define("Grayscale-plural",
    ca = u"Tons de gris",
    es = u"Tonos de gris",
    en = u"Grayscale"
)

# Agreement to terms & conditions
#------------------------------------------------------------------------------
translations.define("woost.controllers.formagreement",
    ca = lambda member:
        u"He llegit i accepto "
        + (
            (
                u"<a href='%s' target='_blank'>els termes i condicions</a> "
                % member.agreement_document.get_uri()
            )
            if member.agreement_document
            else u"els termes i condicions "
        )
        + u"d'aquest formulari",
    es = lambda member:
        u"He leído y acepto "
        + (
            (
                u"<a href='%s' target='_blank'>los términos y condiciones</a> "
                % member.agreement_document.get_uri()
            )
            if member.agreement_document
            else u"los términos y condiciones "
        )
        + u"de este formulario",
    en = lambda member:
        u"I have read and agree to the "
        + (
            (
                u"<a href='%s' target='_blank'>terms and conditions</a> "
                % member.agreement_document.get_uri()
            )
            if member.agreement_document
            else u"terms and conditions "
        )
        + u"of this form"
)

translations.define(
    "woost.controllers.formagreement.ConsentNotGivenError-instance",
    ca = lambda instance:
        u"Has d'acceptar els termes i condicions del formulari",
    es = lambda instance:
        u"Debes aceptar los términos y condiciones de este formulario",
    en = lambda instance:
        u"You must accept the terms & conditions of the form"
)

# BackOfficeItemHeading
#------------------------------------------------------------------------------
translations.define("woost.views.BackOfficeItemHeading.item_path.conjunction",
    ca = u"a",
    es = u"en",
    en = u"in"
)

# BackOfficeReferencesView
#------------------------------------------------------------------------------
translations.define("woost.views.BackOfficeReferencesView.summary",
    ca = lambda count:
        u"Aquest element no és referenciat per cap altre element."
        if not count
        else (
            u"Referenciat per <strong>%d</strong> %s:" % (
                count,
                plural2(count, u"element", u"elements")
            )
        ),
    es = lambda count:
        u"Este elemento no está referenciado por ningún otro elemento."
        if not count
        else (
            u"Referenciado por <strong>%d</strong> %s:" % (
                count,
                plural2(count, u"elemento", u"elementos")
            )
        ),
    en = lambda count:
        u"This element is not referenced by any other element."
        if not count
        else (
            u"Referenced by <strong>%d</strong> %s:" % (
                count,
                plural2(count, u"element", u"elements")
            )
        )
)

translations.define("woost.views.BackOfficeReferencesView.referrer_heading",
    ca = u"Element relacionat",
    es = u"Elemento relacionado",
    en = u"Referrer"
)

translations.define("woost.views.BackOfficeReferencesView.relation_heading",
    ca = u"Relació",
    es = u"Relación",
    en = u"Relation"
)

# VideoPlayerSettings
#------------------------------------------------------------------------------
translations.define("VideoPlayerSettings",
    ca = u"Opcions de reproductor de vídeo",
    es = u"Opciones de reproductor de video",
    en = u"Video player settings"
)

translations.define("VideoPlayerSettings-plural",
    ca = u"Opcions de reproductor de vídeo",
    es = u"Opciones de reproductor de video",
    en = u"Video player settings"
)

translations.define("VideoPlayerSettings.title",
    ca = u"Nom",
    es = u"Nombre",
    en = u"Name"
)

translations.define("VideoPlayerSettings.width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("VideoPlayerSettings.height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

translations.define("VideoPlayerSettings.autoplay",
    ca = u"Iniciar la reproducció automàticament",
    es = u"Iniciar la reproducción automáticamente",
    en = u"Autoplay"
)

translations.define("VideoPlayerSettings.show_player_controls",
    ca = u"Mostrar controls de reproducció",
    es = u"Mostrar controles de reproducción",
    en = u"Show player controls"
)

# BackOfficeInstallationSyncView
#------------------------------------------------------------------------------
translations.define("woost.views.BackOfficeInstallationSyncView.incomming_section",
    ca = u"Contingut nou",
    es = u"Contenido nuevo",
    en = u"New content"
)

translations.define("woost.views.BackOfficeInstallationSyncView.modified_section",
    ca = u"Contingut modificat",
    es = u"Contenido modificado",
    en = u"Modified content"
)

translations.define("woost.views.BackOfficeInstallationSyncView.remote_value",
    ca = lambda installation:
        u"Valor a " + decapitalize(translations(installation)),
    es = lambda installation:
        u"Valor en " + decapitalize(translations(installation)),
    en = lambda installation:
        u"Value in " + decapitalize(translations(installation))
)

translations.define("woost.views.BackOfficeInstallationSyncView.local_value",
    ca = u"Valor local",
    es = u"Valor local",
    en = u"Local value"
)

translations.define("woost.views.BackOfficeInstallationSyncView.diff_dialog_button",
    ca = u"Detalls",
    es = u"Detalles",
    en = u"Details"
)

translations.define(
    "woost.views.BackOfficeInstallationSyncView.sync_request_error",
    ca = lambda error:
        u"S'ha produït un error en intentar accedir a la instal·lació "
        u"remota (%s)" % error,
    es = lambda error:
        u"Se ha producido un error al intentar acceder a la instalación "
        u"remota (%s)" % error,
    en = lambda error:
        u"Error connecting to the remote installation (%s)" % error
)

translations.define(
    "woost.views.BackOfficeInstallationSyncView.no_changes_notice",
    ca = u"No hi ha cap canvi a importar.",
    es = u"No hay cambios a importar.",
    en = u"There are no changes to import."
)

translations.define("woost.views.BackOfficeInstallationSyncView.sync_button",
    ca = u"Importar els canvis seleccionats",
    es = u"Importar los cambios seleccionados",
    en = u"Import selected content"
)

translations.define(
    "woost.views.BackOfficeInstallationSyncView.select_all_button",
    ca = u"Seleccionar-ho tot",
    es = u"Seleccionarlo todo",
    en = u"Select all"
)

translations.define(
    "woost.views.BackOfficeInstallationSyncView.select_none_button",
    ca = u"Buidar la selecció",
    es = u"Vaciar la selección",
    en = u"Empty selection"
)

translations.define(
    "woost.views.BackOfficeInstallationSyncView.file_hash_diff_heading",
    ca = u"Fitxer",
    es = u"Fichero",
    en = u"File"
)

# InstallationSyncController
#------------------------------------------------------------------------------
translations.define("woost.controllers.InstallationSyncController.success",
    ca = u"S'han sincronitzat els continguts indicats.",
    es = u"Se han sincronizado los contenidos indicados.",
    en = u"Successfully synchronized the selected content."
)

# Element types
#------------------------------------------------------------------------------
translations.define("woost.models.ElementType=div",
    ca = u"Element genèric (div)",
    es = u"Elemento genérico (div)",
    en = u"Generic element (div)"
)

translations.define("woost.models.ElementType=section",
    ca = u"Secció",
    es = u"Sección",
    en = u"Section"
)

translations.define("woost.models.ElementType=article",
    ca = u"Article",
    es = u"Artículo",
    en = u"Article"
)

translations.define("woost.models.ElementType=details",
    ca = u"Detalls",
    es = u"Detalles",
    en = u"Details"
)

translations.define("woost.models.ElementType=figure",
    ca = u"Recurs complementari (figure)",
    es = u"Recurso complementario (figure)",
    en = u"Figure"
)

translations.define("woost.models.ElementType=aside",
    ca = u"Contingut relacionat (aside)",
    es = u"Contenido relacionado (aside)",
    en = u"Tangentially related content (aside)"
)

translations.define("woost.models.ElementType=header",
    ca = u"Capçalera",
    es = u"Cabecera",
    en = u"Header"
)

translations.define("woost.models.ElementType=footer",
    ca = u"Peu",
    es = u"Pie",
    en = u"Footer"
)

translations.define("woost.models.ElementType=nav",
    ca = u"Navegació",
    es = u"Navegación",
    en = u"Navigation"
)

translations.define("woost.models.ElementType=dd",
    ca = u"Definició (dd)",
    es = u"Definición (dd)",
    en = u"Definition (dd)"
)

# Block
#------------------------------------------------------------------------------
translations.define("Block",
    ca = u"Bloc",
    es = u"Bloque",
    en = u"Block"
)

translations.define("Block-plural",
    ca = u"Blocs",
    es = u"Bloques",
    en = u"Blocks"
)

translations.define("Block.content",
    ca = u"Contingut",
    es = u"Contenido",
    en = u"Content"
)

translations.define("Block.behavior",
    ca = u"Comportament",
    es = u"Comportamiento",
    en = u"Behavior"
)

translations.define("Block.html",
    ca = u"HTML",
    es = u"HTML",
    en = u"HTML"
)

translations.define("Block.heading",
    ca = u"Encapçalament",
    es = u"Encabezado",
    en = u"Heading"
)

translations.define("Block.heading_type",
    ca = u"Tipus d'encapçalament",
    es = u"Tipo de encabezado",
    en = u"Heading type"
)

translations.define("Block.heading_type=hidden",
    ca = u"Ocult",
    es = u"Oculto",
    en = u"Hidden"
)

translations.define("Block.heading_type=generic",
    ca = u"Etiqueta genèrica (div)",
    es = u"Etiqueta genérica (div)",
    en = u"Generic label (div)"
)

translations.define("Block.heading_type=hidden_h1",
    ca = u"Encapçalament de secció ocult",
    es = u"Encabezado de sección oculto",
    en = u"Hidden section heading"
)

for level in range(1, 7):
    translations.define("Block.heading_type=h" + str(level),
        ca = u"Encapçalament %d" % level,
        es = u"Encabezado %d" % level,
        en = u"Heading %d" % level
    )

translations.define("Block.heading_type=dt",
    ca = u"Terme (dt)",
    es = u"Término (dt)",
    en = u"Term (dt)"
)

translations.define("Block.heading_type=figcaption",
    ca = u"Títol per un recurs complementari (figcaption)",
    es = u"Título para un recurso complementario (figcaption)",
    en = u"Figure caption"
)

translations.define("Block.html_attributes",
    ca = u"Atributs HTML",
    es = u"Atributos HTML",
    en = u"HTML attributes"
)

translations.define("Block.styles",
    ca = u"Estils",
    es = u"Estilos",
    en = u"Styles"
)

translations.define("Block.inline_css_styles",
    ca = u"Estils en línia",
    es = u"Estilos en linea",
    en = u"Inline CSS styles"
)

translations.define("Block.per_language_publication",
    ca = u"Publicació per idiomes",
    es = u"Publicación por idiomas",
    en = u"Per language publication"
)

translations.define("Block.enabled",
    ca = u"Actiu",
    es = u"Activo",
    en = u"Active"
)

translations.define("Block.enabled_translations",
    ca = u"Traduccions actives",
    es = u"Traducciones actives",
    en = u"Enabled translations"
)

translations.define("Block.start_date",
    ca = u"Inici de publicació",
    es = u"Inicio de publicación",
    en = u"Publication start"
)

translations.define("Block.end_date",
    ca = u"Fi de publicació",
    es = u"Fin de publicación",
    en = u"Publication end"
)

translations.define("Block.controller",
    ca = u"Controlador",
    es = u"Controlador",
    en = u"Controller"
)

translations.define("Block.initialization",
    ca = u"Inicialització",
    es = u"Inicialización",
    en = u"Initialization"
)

translations.define("Block.initialization-explanation",
    ca = u"""
        <p>
            Fragment de codi Python que permet inicialitzar la vista generada
            pel bloc.
        </p>
        <details>
            <summary>Detalls</summary>
            <p>
                Es proporcionen les variables següents:
            </p>
            <dl>
                <dt>block</dt>
                <dd>Una referència a aquest bloc.</dd>
                <dt>view</dt>
                <dd>La vista a inicialitzar.</dd>
            </dl>
        </details>
        """,
    es = u"""
        <p>
            Fragmento de código Python que permite inicializar la vista generada
            por el bloque.
        </p>
        <details>
            <summary>Detalles</summary>
            <p>
                Se proporcionan las variables siguientes:
            </p>
            <dl>
                <dt>block</dt>
                <dd>Una referencia a este bloque.</dd>
                <dt>view</dt>
                <dd>La vista a inicializar.</dd>
            </dl>
        </details>
        """,
    en = u"""
        <p>
            A Python code snippet to initialize the view generated by this
            block.
        </p>
        <details>
            <summary>Details</summary>
            <p>
                The code snippet will have access to the following variables:
            </p>
            <dl>
                <dt>block</dt>
                <dd>A reference to this block.</dd>
                <dt>view</dt>
                <dd>The view to initialize.</dd>
            </dl>
        </details>
        """
)


# CustomBlock
#------------------------------------------------------------------------------
translations.define("CustomBlock",
    ca = u"Bloc a mida",
    es = u"Bloque a medida",
    en = u"Custom block"
)

translations.define("CustomBlock-plural",
    ca = u"Blocs a mida",
    es = u"Bloques a medida",
    en = u"Custom blocks"
)

translations.define("CustomBlock.view_class",
    ca = u"Vista",
    es = u"Vista",
    en = u"View"
)

translations.define("CustomBlock.view_class-explanation",
    ca = u"Nom qualificat de la vista CML a mostrar",
    es = u"Nombre cualificado de la vista CML a mostrar",
    en = u"The qualified name of the CML view to display"
)

# ContainerBlock
#------------------------------------------------------------------------------
translations.define("ContainerBlock",
    ca = u"Contenidor",
    es = u"Contenedor",
    en = u"Container"
)

translations.define("ContainerBlock-plural",
    ca = u"Contenidors",
    es = u"Contenedores",
    en = u"Containers"
)

translations.define("ContainerBlock.blocks",
    ca = u"Blocs fills",
    es = u"Bloques hijos",
    en = u"Child blocks"
)

translations.define("ContainerBlock.element_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Element type"
)

translations.define("ContainerBlock.list_type",
    ca = u"Tipus de llista",
    es = u"Tipo de lista",
    en = u"List type"
)

translations.define("ContainerBlock.list_type=div",
    ca = u"Element genèric (div)",
    es = u"Elemento genérico (div)",
    en = u"Generic element (div)"
)

translations.define("ContainerBlock.list_type=ul",
    ca = u"Llista",
    es = u"Lista",
    en = u"List"
)

translations.define("ContainerBlock.list_type=ol",
    ca = u"Llista ordenada",
    es = u"Lista ordenada",
    en = u"Ordered list"
)

translations.define("ContainerBlock.list_type=dl",
    ca = u"Llista de definició",
    es = u"Lista de definición",
    en = u"Definition list"
)

# SlideShowBlock
#------------------------------------------------------------------------------
translations.define("SlideShowBlock",
    ca = u"Passador",
    es = u"Pasador",
    en = u"Slide show"
)

translations.define("SlideShowBlock-plural",
    ca = u"Passadors",
    es = u"Pasadores",
    en = u"Slide shows"
)

translations.define("SlideShowBlock.element_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Element type"
)

translations.define("SlideShowBlock.slides",
    ca = u"Diapositives",
    es = u"Diapositivas",
    en = u"Slides"
)

translations.define("SlideShowBlock.transition_settings",
    ca = u"Transicions",
    es = u"Transiciones",
    en = u"Transitions"
)

translations.define("SlideShowBlock.autoplay",
    ca = u"Transicions automàtiques",
    es = u"Transiciones automáticas",
    en = u"Autoplay"
)

translations.define("SlideShowBlock.controls",
    ca = u"Controls",
    es = u"Controles",
    en = u"Controls"
)

translations.define("SlideShowBlock.navigation_controls",
    ca = u"Mostrar controls de navegació",
    es = u"Mostrar controles de navegación",
    en = u"Show navigation controls"
)

translations.define("SlideShowBlock.bullet_controls",
    ca = u"Mostrar botons de diapositiva",
    es = u"Mostrar botones de diapositiva",
    en = u"Show slide bullets"
)

translations.define("SlideShowBlock.bullet_view_class",
    ca = u"Aparença dels botons de diapositiva",
    es = u"Apariencia de los botones de diapositiva",
    en = u"Slide bullets appearence"
)

translations.define(
    "SlideShowBlock.bullet_view_class=woost.views.SlideShowButtonBullet",
    ca = u"Botó",
    es = u"Botón",
    en = u"Button"
)

translations.define(
    "SlideShowBlock.bullet_view_class=woost.views.SlideShowTextBullet",
    ca = u"Text",
    es = u"Texto",
    en = u"Text"
)

translations.define(
    "SlideShowBlock.bullet_view_class=woost.views.SlideShowImageBullet",
    ca = u"Imatge",
    es = u"Imagen",
    en = u"Image"
)

translations.define(
    "SlideShowBlock.bullet_view_class=woost.views.SlideShowTextAndImageBullet",
    ca = u"Imatge i text",
    es = u"Imagen y texto",
    en = u"Image and text"
)

translations.define("SlideShowBlock.bullet_image_factory",
    ca = u"Processat d'imatge pels botons de diapositiva",
    es = u"Procesado de imagen para los botones de diapositiva",
    en = u"Image processing for slide bullets"
)

translations.define("SlideShowBlock.interval",
    ca = u"Freqüència de les transicions",
    es = u"Frecuencia de las transiciones",
    en = u"Time between transitions"
)

translations.define("SlideShowBlock.interval-explanation",
    ca = u"Si s'activen les transicions automàtiques, indica el nombre de "
         u"milisegons abans que el bloc passi a la següent diapositiva.",
    es = u"Si se activan las transiciones automáticas, indica el número de "
         u"milisegundos antes que el bloque pase a la diapositiva siguiente.",
    en = u"If autoplay is enabled, indicates the number of milliseconds that "
         u"pass between automatic transitions."
)

translations.define("SlideShowBlock.transition_duration",
    ca = u"Duració de les transicions",
    es = u"Duración de las transiciones",
    en = u"Transition duration"
)

translations.define("SlideShowBlock.transition_duration-explanation",
    ca = u"Especifica la duració de l'efecte de transició, en milisegons",
    es = u"Especifica la duración del efecto de transición, en milisegundos",
    en = u"Sets the duration of the slide transition effect, in milliseconds"
)

translations.define("SlideShowBlock.transition_effect",
    ca = u"Efecte de transició",
    es = u"Efecto de transición",
    en = u"Transition effect"
)

translations.define("SlideShowBlock.transition_effect=fade",
    ca = u"Fondre",
    es = u"Fundir",
    en = u"Fade"
)

translations.define("SlideShowBlock.transition_effect=topBottomSlide",
    ca = u"Lliscar de dalt a baix",
    es = u"Deslizar de arriba abajo",
    en = u"Top-bottom slide"
)

# MenuBlock
#------------------------------------------------------------------------------
translations.define("MenuBlock",
    ca = u"Menú",
    es = u"Menú",
    en = u"Menu"
)

translations.define("MenuBlock-plural",
    ca = u"Menús",
    es = u"Menús",
    en = u"Menus"
)

translations.define("MenuBlock.root",
    ca = u"Arrel",
    es = u"Raiz",
    en = u"Root"
)

translations.define("MenuBlock.root_visible",
    ca = u"Arrel visible",
    es = u"Raiz visible",
    en = u"Root visible"
)

translations.define("MenuBlock.max_depth",
    ca = u"Profunditat màxima",
    es = u"Profundidad máxima",
    en = u"Maximum depth"
)

translations.define("MenuBlock.expanded",
    ca = u"Expandit",
    es = u"Expandido",
    en = u"Expanded"
)

# HTMLBlock
#------------------------------------------------------------------------------
translations.define("HTMLBlock",
    ca = u"HTML",
    es = u"HTML",
    en = u"HTML"
)

translations.define("HTMLBlock-plural",
    ca = u"HTML",
    es = u"HTML",
    en = u"HTML"
)

translations.define("HTMLBlock.html",
    ca = u"HTML",
    es = u"HTML",
    en = u"HTML"
)

translations.define("HTMLBlock.translated_html",
    ca = u"HTML per idioma",
    es = u"HTML por idioma",
    en = u"Per language HTML"
)

translations.define("HTMLBlock.translated_html-explanation",
    ca = u"Utilitzar només si cal diferenciar l'HTML produït en un idioma "
         u"concret. Pels idiomes en que es deixi buit, s'utilitzarà el valor "
         u"del camp <em>HTML</em>.",
    es = u"Utilizar únicamente si es necesario distinguir el HTML producido "
         u"en un idioma concreto. En aquellos idiomas en que se deje vacío "
         u"se utilizará el valor del campo <em>HTML</em>.",
    en = u"Use only to differentiate the HTML produced for specific "
         u"languages. In languages where it is left blank, the content of the "
         u"<em>HTML</em> field will be used instead."
)

# TextBlock
#------------------------------------------------------------------------------
translations.define("TextBlock",
    ca = u"Text + imatges",
    es = u"Texto + imágenes",
    en = u"Text + images"
)

translations.define("TextBlock-plural",
    ca = u"Text + imatges",
    es = u"Texto + imágenes",
    en = u"Text + images"
)

translations.define("TextBlock.heading_alignment",
    ca = u"Disposició de l'encapçalament",
    es = u"Disposición del encabezado",
    en = u"Heading alignment"
)

translations.define("TextBlock.heading_alignment=top",
    ca = u"Inici del bloc",
    es = u"Inicio del bloque",
    en = u"Top"
)

translations.define("TextBlock.heading_alignment=inside",
    ca = u"Inici del text",
    es = u"Inicio del texto",
    en = u"Start of the text"
)

translations.define("TextBlock.element_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Element type"
)

translations.define("TextBlock.link",
    ca = u"Enllaç",
    es = u"Enlace",
    en = u"Link"
)

translations.define("TextBlock.link_destination",
    ca = u"Destí de l'enllaç",
    es = u"Destino del enlace",
    en = u"Linked resource"
)

translations.define("TextBlock.link_parameters",
    ca = u"Paràmetres addicionals per l'enllaç",
    es = u"Parámetros adicionales para el enlace",
    en = u"Additional URL parameters"
)

translations.define("TextBlock.link_parameters-explanation",
    ca = u"Un paràmetre per línia, separant el nom i el valor amb un caràcter "
         u"'='",
    es = u"Un parámetro por linea, separando el nombre y el valor con un "
         u"caracter '='",
    en = u"One parameter per line, with key and value separated by a "
         u"'=' character"
)

translations.define("TextBlock.link_opens_in_new_window",
    ca = u"Obrir l'enllaç a una nova finestra",
    es = u"Abrir el enlace en una ventana nueva",
    en = u"Open the link in a new window"
)

translations.define("TextBlock.text",
    ca = u"Text",
    es = u"Texto",
    en = u"Text"
)

translations.define("TextBlock.images",
    ca = u"Imatges",
    es = u"Imágenes",
    en = u"Images"
)

translations.define("TextBlock.image_alignment",
    ca = u"Disposició de les imatges",
    es = u"Disposición de las imágenes",
    en = u"Image alignment"
)

translations.define("TextBlock.image_alignment=float_top_left",
    ca = u"Flotar a l'esquerra",
    es = u"Flotar a la izquierda",
    en = u"Top left, floating"
)

translations.define("TextBlock.image_alignment=float_top_right",
    ca = u"Flotar a la dreta",
    es = u"Flotar a la derecha",
    en = u"Top right, floating"
)

translations.define("TextBlock.image_alignment=column_left",
    ca = u"Columna a l'esquerra",
    es = u"Columna a la izquierda",
    en = u"Top left, in their own column"
)

translations.define("TextBlock.image_alignment=column_right",
    ca = u"Columna a la dreta",
    es = u"Columna a la derecha",
    en = u"Top right, in their own column"
)

translations.define("TextBlock.image_alignment=top_left",
    ca = u"A dalt a l'esquerra",
    es = u"Arriba a la izquierda",
    en = u"Top left"
)

translations.define("TextBlock.image_alignment=bottom_left",
    ca = u"A sota a l'esquerra",
    es = u"Abajo a la izquierda",
    en = u"Bottom left"
)

translations.define("TextBlock.image_alignment=center_top",
    ca = u"Centrar a dalt",
    es = u"Centrar arriba",
    en = u"Top center"
)

translations.define("TextBlock.image_alignment=center_bottom",
    ca = u"Centrar a sota",
    es = u"Centrar abajo",
    en = u"Bottom center"
)

translations.define("TextBlock.image_alignment=top_right",
    ca = u"A dalt a la dreta",
    es = u"Arriba a la derecha",
    en = u"Top right"
)

translations.define("TextBlock.image_alignment=inline",
    ca = u"En línia",
    es = u"En linea",
    en = u"Inline"
)

translations.define("TextBlock.image_alignment=heading_icon",
    ca = u"Precedint l'encapçalament",
    es = u"Precediendo el encabezado",
    en = u"Preceding the heading"
)

translations.define("TextBlock.image_alignment=background",
    ca = u"Imatge de fons",
    es = u"Imagen de fondo",
    en = u"Background image"
)

translations.define("TextBlock.image_alignment=fallback",
    ca = u"Imatge amb descripció textual substitutiva",
    es = u"Imagen con descripción textual sustitutiva",
    en = u"Image with fallback content"
)

translations.define("TextBlock.image_thumbnail_factory",
    ca = u"Processat de les imatges",
    es = u"Procesado de las imágenes",
    en = u"Image processing"
)

translations.define("TextBlock.image_close_up_enabled",
    ca = u"Ampliar les imatges en fer-hi clic",
    es = u"Ampliar las imágenes al pulsarlas",
    en = u"Click to enlarge"
)

translations.define("TextBlock.image_close_up_factory",
    ca = u"Processat de les imatges ampliades",
    es = u"Procesado de las imágenes ampliadas",
    en = u"Image processing for enlarged images"
)

translations.define("TextBlock.image_close_up_preload",
    ca = u"Precàrrega de les imatges ampliades",
    es = u"Precarga de las imágenes ampliadas",
    en = u"Preload enlarged images"
)

translations.define("TextBlock.image_labels_visible",
    ca = u"Mostrar els títols de les imatges",
    es = u"Mostrar los títulos de las imágenes",
    en = u"Show image titles"
)

translations.define("TextBlock.image_footnotes_visible",
    ca = u"Mostrar els peus d'imatge",
    es = u"Mostrar los pies de imagen",
    en = u"Show image footnotes"
)

translations.define("TextBlock.image_original_link_visible",
    ca = u"Mostrar un enllaç a la imatge sense modificar",
    es = u"Mostrar un enlace a la imagen sin modificar",
    en = u"Show a link to the original image"
)

# VideoBlock
#------------------------------------------------------------------------------
translations.define("VideoBlock",
    ca = u"Vídeo",
    es = u"Video",
    en = u"Video"
)

translations.define("VideoBlock-plural",
    ca = u"Vídeos",
    es = u"Vídeos",
    en = u"Videos"
)

translations.define("VideoBlock.element_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Element type"
)

translations.define("VideoBlock.video",
    ca = u"Vídeo",
    es = u"Video",
    en = u"Video"
)

translations.define("VideoBlock.player_settings",
    ca = u"Opcions de reproductor de vídeo",
    es = u"Opciones de reproductor de video",
    en = u"Video player settings"
)

translations.define("VideoBlock.view_class",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define("VideoBlock.view_class=woost.views.VideoBlockView",
    ca = u"Incrustat",
    es = u"Incrustado",
    en = u"Embedded"
)

translations.define("VideoBlock.view_class=woost.views.VideoPopUp",
    ca = u"Finestra emergent",
    es = u"Ventana emergente",
    en = u"Pop up"
)

# TwitterTimelineBlock
#------------------------------------------------------------------------------
translations.define("TwitterTimelineBlock",
    ca = u"Missatges de Twitter",
    es = u"Mensajes de Twitter",
    en = u"Twitter timeline"
)

translations.define("TwitterTimelineBlock-plural",
    ca = u"Missatges de Twitter",
    es = u"Mensajes de Twitter",
    en = u"Twitter timeline"
)

translations.define("TwitterTimelineBlock.tweet",
    ca = u"Tuit",
    es = u"Tuit",
    en = u"Tweet"
)

translations.define("TwitterTimelineBlock.appearence",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define("TwitterTimelineBlock.widget_id",
    ca = u"ID del widget",
    es = u"ID del widget",
    en = u"Widget ID"
)

translations.define("TwitterTimelineBlock.theme",
    ca = u"Plantilla",
    es = u"Plantilla",
    en = u"Theme"
)

translations.define("TwitterTimelineBlock.theme=light",
    ca = u"Clar",
    es = u"Claro",
    en = u"Light"
)

translations.define("TwitterTimelineBlock.theme=dark",
    ca = u"Fosc",
    es = u"Oscuro",
    en = u"Dark"
)

translations.define("TwitterTimelineBlock.link_color",
    ca = u"Color de l'enllaç",
    es = u"Color del enlace",
    en = u"Link color"
)

translations.define("TwitterTimelineBlock.width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("TwitterTimelineBlock.height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

translations.define("TwitterTimelineBlock.related_accounts",
    ca = u"Comptes relacionats",
    es = u"Cuentas relacionadas",
    en = u"Related accounts"
)

# LoginBlock
#------------------------------------------------------------------------------
translations.define("LoginBlock",
    ca = u"Formulari d'autenticació d'usuari",
    es = u"Formulario de autenticación de usuario",
    en = u"Login form"
)

translations.define("LoginBlock-plural",
    ca = u"Formularis d'autenticació d'usuari",
    es = u"Formularios de autenticación de usuario",
    en = u"Login forms"
)

translations.define("LoginBlock.login_target",
    ca = u"Pàgina de destí",
    es = u"Página de destino",
    en = u"Destination page"
)

translations.define("LoginBlock.login_target-explanation",
    ca = u"La pàgina que rebrà la petició d'autenticació de l'usuari",
    es = u"La pàgina que recibirá la petición de autenticación del "
         u"usuario",
    en = u"The page that will handle the user's authentication request"
)

translations.define("LoginBlockForm.user",
    ca = u"Usuari",
    es = u"Usuario",
    en = u"User",
    pt = u"Usuário"
)

translations.define("LoginBlockForm.password",
    ca = u"Contrasenya",
    es = u"Contraseña",
    en = u"Password",
    pt = u"Chave de acesso"
)

translations.define("woost.views.LoginBlockView.submit_button",
    ca = u"Entrar",
    es = u"Entrar",
    en = u"Login",
    pt = u"Entrar"
)

# IFrameBlock
#------------------------------------------------------------------------------
translations.define("IFrameBlock",
    ca = u"IFrame",
    es = u"IFrame",
    en = u"IFrame"
)

translations.define("IFrameBlock-plural",
    ca = u"IFrames",
    es = u"IFrames",
    en = u"IFrames"
)

translations.define("IFrameBlock.src",
    ca = u"Adreça a mostrar",
    es = u"Dirección a mostrar",
    en = u"Content URL"
)

translations.define("IFrameBlock.width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("IFrameBlock.height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

# EditBlocksView
#------------------------------------------------------------------------------
translations.define("woost.views.EditBlocksView.body_header",
    ca = lambda item:
        u"Editant els blocs " + ca_possessive(translations(item)),
    es = lambda item:
        u"Editando los bloques de " + translations(item),
    en = lambda item:
        u"Editing the blocks for " + translations(item)
)

# EditBlocksSlotList
#------------------------------------------------------------------------------
translations.define(
    "woost.views.EditBlocksSlotList.new_blocks_panel.panel_header",
    ca = u"Crear un nou bloc",
    es = u"Crear un bloque nuevo",
    en = u"Create a new block"
)

translations.define(
    "woost.views.EditBlocksSlotList.common_blocks_panel.panel_header",
    ca = u"Afegir un bloc existent",
    es = u"Añadir un bloque existente",
    en = u"Add an existing block"
)

translations.define(
    "woost.views.EditBlocksSlotList.dialog_buttons.cancel_button",
    ca = u"Cancel·lar",
    es = u"Cancelar",
    en = u"Cancel"
)

# BlockDisplay
#------------------------------------------------------------------------------
translations.define("woost.views.BlockDisplay.common_status.label",
    ca = u"Comú",
    es = u"Común",
    en = u"Common"
)

translations.define("woost.views.BlockDisplay.common_status.title",
    ca = u"Aquest bloc resideix a la llibreria de blocs comuns, i pot "
         u"aparèixer a més d'una pàgina",
    es = u"Este bloque reside en la libreria de bloques comunes, pudiendo "
         u"aparecer en más de una página",
    en = u"This block resides within the site's common blocks gallery, and "
         u"it may appear in more than one page"
)

translations.define("woost.views.BlockDisplay.disabled_status.label",
    ca = u"Inactiu",
    es = u"Inactivo",
    en = u"Disabled"
)

translations.define("woost.views.BlockDisplay.disabled_status.title",
    ca = u"Aquest bloc està deshabilitat, no s'inclourà a la pàgina",
    es = u"Este bloque está deshabilitado, no se incluirá en la página",
    en = u"This block is disabled and won't be displayed in the page"
)

translations.define("woost.views.BlockDisplay.expired_status.label",
    ca = u"Expirat",
    es = u"Expirado",
    en = u"Expired"
)

translations.define("woost.views.BlockDisplay.expired_status.title",
    ca = u"Aquest bloc ha assolit la seva data d'expiració i ha deixat d'estar "
         u"visible",
    es = u"Este bloque ha alcanzado su fecha de expiración y ha dejado de "
         u"estar visible",
    en = u"This block has reached its expiration date and is no longer visible"
)

translations.define(
    "woost.views.BlockDisplay.awaiting_publication_status.label",
    ca = u"Esperant inici de publicació",
    es = u"Esperando inicio de publicación",
    en = u"Awaiting start of publication"
)

translations.define(
    "woost.views.BlockDisplay.awaiting_publication_status.title",
    ca = u"Aquest bloc no ha assolit la seva data d'inici de publicació i "
         u"encara no és visible",
    es = u"Este bloque no ha alcanzado su fecha de inicio de publicación y "
         u"todavía no es visible",
    en = u"This block has not reached its publication date and is not "
         u"visible yet"
)

translations.define("woost.views.BlockDisplay.temporary_status.label",
    ca = u"Temporal",
    es = u"Temporal",
    en = u"Temporary"
)

translations.define("woost.views.BlockDisplay.temporary_status.title",
    ca = u"Aquest bloc es publica només durant una finestra de temps",
    es = u"Este bloque solo se publicada durante una ventana de tiempo",
    en = u"This block is only published during a certain time window"
)

translations.define("woost.block_clipboard.empty",
    ca = u"El portaretalls no conté cap bloc",
    es = u"El portapapeles no cotiene ningún bloque",
    en = u"The clipboard is empty"
)

translations.define("woost.block_clipboard.error",
    ca = u"El contingut del portaretalls no és vàlid",
    es = u"El contenido del portapapeles no es válido",
    en = u"The clipboard content is not valid"
)

# NewsListing
#------------------------------------------------------------------------------
translations.define("NewsListing",
    ca = u"Llistat de notícies",
    es = u"Listado de noticias",
    en = u"News listing"
)

translations.define("NewsListing-plural",
    ca = u"Llistats de notícies",
    es = u"Listados de noticias",
    en = u"News listings"
)

translations.define("NewsListing.listing",
    ca = u"Llistat",
    es = u"Listado",
    en = u"Listing"
)

translations.define("NewsListing.element_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Element type"
)

translations.define("NewsListing.paginated",
    ca = u"Paginar els resultats",
    es = u"Paginar los resultados",
    en = u"Paginate results"
)

translations.define("NewsListing.page_size",
    ca = u"Mida del llistat",
    es = u"Tamaño del listado",
    en = u"Listing size"
)

translations.define("NewsListing.view_class",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define(
    "NewsListing.view_class=woost.views.CompactNewsListing",
    ca = u"Compacta",
    es = u"Compacta",
    en = u"Compact"
)

translations.define(
    "NewsListing.view_class=woost.views.TextOnlyNewsListing",
    ca = u"Només text",
    es = u"Solo texto",
    en = u"Text only"
)

translations.define(
    "NewsListing.view_class=woost.views.TextAndImageNewsListing",
    ca = u"Text i imatge",
    es = u"Texto e imagen",
    en = u"Text and image"
)

# EventListing
#------------------------------------------------------------------------------
translations.define("EventListing",
    ca = u"Llistat d'esdeveniments",
    es = u"Listado de eventos",
    en = u"Event listing"
)

translations.define("EventListing-plural",
    ca = u"Llistats d'events",
    es = u"Listados de eventos",
    en = u"Event listings"
)

translations.define("EventListing.listing",
    ca = u"Llistat",
    es = u"Listado",
    en = u"Listing"
)

translations.define("EventListing.element_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Element type"
)

translations.define("EventListing.include_expired",
    ca = u"Incloure esdeveniments passats",
    es = u"Incluir eventos pasados",
    en = u"Include expired events"
)

translations.define("EventListing.listing_order",
    ca = u"Ordenació",
    es = u"Ordenación",
    en = u"Order"
)

translations.define("EventListing.listing_order=event_start",
    ca = u"Data d'inici, ascendent",
    es = u"Fecha de inicio, ascendente",
    en = u"Event start, ascending"
)

translations.define("EventListing.listing_order=-event_start",
    ca = u"Data d'inici, descendent",
    es = u"Fecha de inicio, descendente",
    en = u"Event start, descending"
)

translations.define("EventListing.paginated",
    ca = u"Paginar els resultats",
    es = u"Paginar los resultados",
    en = u"Paginate results"
)

translations.define("EventListing.page_size",
    ca = u"Mida del llistat",
    es = u"Tamaño del listado",
    en = u"Listing size"
)

translations.define("EventListing.view_class",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define(
    "EventListing.view_class=woost.views.CompactEventListing",
    ca = u"Només el títol",
    es = u"Solo el título",
    en = u"Title only"
)

translations.define(
    "EventListing.view_class=woost.views.DateLocationTitleEventListing",
    ca = u"Data, ubicació i títol",
    es = u"Fecha, ubicación y título",
    en = u"Date, location and title"
)

translations.define(
    "EventListing.view_class=woost.views.EventsCalendar",
    ca = u"Calendari mensual",
    es = u"Calendario mensual",
    en = u"Monthly calendar"
)

# EventsCalendar
#------------------------------------------------------------------------------
translations.define("woost.views.EventsCalendar.previous_month_link",
    ca = u"Mes anterior",
    es = u"Mes anterior",
    en = u"Previous month"
)

translations.define("woost.views.EventsCalendar.next_month_link",
    ca = u"Mes següent",
    es = u"Mes siguiente",
    en = u"Next month"
)

translations.define("woost.views.EventsCalendar.previous_year_link",
    ca = u"Any anterior",
    es = u"Año anterior",
    en = u"Previous year"
)

translations.define("woost.views.EventsCalendar.next_year_link",
    ca = u"Any següent",
    es = u"Año siguiente",
    en = u"Next year"
)

# FacebookLikeButton
#------------------------------------------------------------------------------
translations.define("FacebookLikeButton",
    ca = u'Botó de "M\'agrada" de Facebook',
    es = u'Botón de "Me gusta" de Facebook',
    en = u"Facebook Like button"
)

translations.define("FacebookLikeButton-plural",
    ca = u'Botons de "M\'agrada" de Facebook',
    es = u'Botones de "Me gusta" de Facebook',
    en = u"Facebook Like buttons"
)

translations.define("FacebookLikeButton.appearence",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define("FacebookLikeButton.fb_href",
    ca = u"Recurs",
    es = u"Recurso",
    en = u"Resource"
)

translations.define("FacebookLikeButton.fb_href-explanation",
    ca = u"La pàgina a recomanar. Deixar en blanc per seleccionar la pàgina on "
         u"es trobi el botó.",
    es = u"La página a recomendar. Dejar en blanco para seleccionar la página "
         u"donde se ubique el botón.",
    en = u"The resource to like. Leave blank to assume the page that contains "
         u"the button."
)

translations.define("FacebookLikeButton.fb_send",
    ca = u"Mostrar el botó d'enviar",
    es = u"Mostrar el botón de enviar",
    en = u"Show the Send button"
)

translations.define("FacebookLikeButton.fb_layout",
    ca = u"Disposició",
    es = u"Disposición",
    en = u"Layout"
)

translations.define("FacebookLikeButton.fb_layout=standard",
    ca = u"Estàndard",
    es = u"Estándar",
    en = u"Standard"
)

translations.define("FacebookLikeButton.fb_layout=button_count",
    ca = u"Recompte",
    es = u"Recuento",
    en = u"Button count"
)

translations.define("FacebookLikeButton.fb_layout=box_count",
    ca = u"Recompte en caixa vertical",
    es = u"Recuento con caja vertical",
    en = u"Box count"
)

translations.define("FacebookLikeButton.fb_show_faces",
    ca = u"Mostrar cares",
    es = u"Mostrar caras",
    en = u"Show faces"
)

translations.define("FacebookLikeButton.fb_width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("FacebookLikeButton.fb_action",
    ca = u"Verb",
    es = u"Verbo",
    en = u"Verb"
)

translations.define("FacebookLikeButton.fb_action=like",
    ca = u"M'agrada",
    es = u"Me gusta",
    en = u"Like"
)

translations.define("FacebookLikeButton.fb_action=recommend",
    ca = u"Recomanar",
    es = u"Recomendar",
    en = u"Recommend"
)

translations.define("FacebookLikeButton.fb_font",
    ca = u"Font",
    es = u"Fuente",
    en = u"Font"
)

translations.define("FacebookLikeButton.fb_colorscheme",
    ca = u"Esquema de colors",
    es = u"Esquema de colores",
    en = u"Colorscheme"
)

translations.define("FacebookLikeButton.fb_colorscheme=light",
    ca = u"Clar",
    es = u"Claro",
    en = u"Light"
)

translations.define("FacebookLikeButton.fb_colorscheme=dark",
    ca = u"Fosc",
    es = u"Oscuro",
    en = u"Dark"
)

translations.define("FacebookLikeButton.fb_ref",
    ca = u"Codi de seguiment",
    es = u"Código de seguimiento",
    en = u"Referral tracking label"
)

# FacebookLikeBox
#------------------------------------------------------------------------------
translations.define("FacebookLikeBox",
    ca = u'Caixa de "M\'agrada" de Facebook',
    es = u'Caja de "Me gusta" de Facebook',
    en = u"Facebook Like Box"
)

translations.define("FacebookLikeBox-plural",
    ca = u'Caixes de "M\'agrada" per pàgines de Facebook',
    es = u'Cajas de "Me gusta" para páginas de Facebook',
    en = u"Facebook Like Boxes"
)

translations.define("FacebookLikeBox.appearence",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define("FacebookLikeBox.fb_href",
    ca = u"Pàgina de Facebook",
    es = u"Página de Facebook",
    en = u"Facebook page"
)

translations.define("FacebookLikeBox.fb_show_faces",
    ca = u"Mostrar cares",
    es = u"Mostrar caras",
    en = u"Show faces"
)

translations.define("FacebookLikeBox.fb_stream",
    ca = u"Mostrar entrades del mur",
    es = u"Mostrar entradas del muro",
    en = u"Show stream"
)

translations.define("FacebookLikeBox.fb_header",
    ca = u"Mostrar el logo de Facebook",
    es = u"Mostrar el logo de Facebook",
    en = u"Show Facebook's logo"
)

translations.define("FacebookLikeBox.fb_width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("FacebookLikeBox.fb_height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

translations.define("FacebookLikeBox.fb_border_color",
    ca = u"Color de la vora",
    es = u"Color del borde",
    en = u"Border color"
)

translations.define("FacebookLikeBox.fb_colorscheme",
    ca = u"Esquema de colors",
    es = u"Esquema de colores",
    en = u"Colorscheme"
)

translations.define("FacebookLikeBox.fb_colorscheme=light",
    ca = u"Clar",
    es = u"Claro",
    en = u"Light"
)

translations.define("FacebookLikeBox.fb_colorscheme=dark",
    ca = u"Fosc",
    es = u"Oscuro",
    en = u"Dark"
)

# TweetButton
#------------------------------------------------------------------------------
translations.define("TweetButton",
    ca = u"Botó de Twitter",
    es = u"Botón de Twitter",
    en = u"Twitter button"
)

translations.define("TweetButton-plural",
    ca = u"Botons de Twitter",
    es = u"Botones de Twitter",
    en = u"Twitter buttons"
)

translations.define("TweetButton.tweet",
    ca = u"Tuit",
    es = u"Tuit",
    en = u"Tweet"
)

translations.define("TweetButton.appearence",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define("TweetButton.tw_target",
    ca = u"Element a compartir",
    es = u"Elemento a compartir",
    en = u"Element to tweet"
)

translations.define("TweetButton.tw_target-explanation",
    ca = u"Deixar en blanc per compartir la pàgina on s'ubiqui el botó",
    es = u"Dejar en blanco para compartir la página donde se ubique el "
         u"botón",
    en = u"Leave blank to tweet the same page where the button resides"
)

translations.define("TweetButton.tw_via",
    ca = u"Via",
    es = u"Via",
    en = u"Via"
)

translations.define("TweetButton.tw_via-explanation",
    ca = u"Nom d'usuari al que s'atribuirà el tuit",
    es = u"Nombre de usuario al que se atribuirá el tuit",
    en = u"Screen name of the user to attribute the Tweet to"
)

translations.define("TweetButton.tw_related",
    ca = u"Comptes relacionats",
    es = u"Cuentas relacionadas",
    en = u"Related accounts"
)

translations.define("TweetButton.tw_hashtags",
    ca = u"Hashtags",
    es = u"Hashtags",
    en = u"Hashtag"
)

translations.define("TweetButton.tw_dnt",
    ca = u"Deshabilitar el seguiment de Twitter",
    es = u"Deshabilitar el seguimiento de Twitter",
    en = u"Opt out of Twitter tailoring"
)

translations.define("TweetButton.tw_text",
    ca = u"Text per defecte",
    es = u"Texto por defecto",
    en = u"Default text for the Tweet"
)

translations.define("TweetButton.tw_size",
    ca = u"Mida del botó",
    es = u"Tamaño del botón",
    en = u"Button size"
)

translations.define("TweetButton.tw_size=medium",
    ca = u"Mitjana",
    es = u"Mediana",
    en = u"Medium"
)

translations.define("TweetButton.tw_size=big",
    ca = u"Gran",
    es = u"Grande",
    en = u"Big"
)

translations.define("TweetButton.tw_count",
    ca = u"Recompte",
    es = u"Recuento",
    en = u"Count"
)

translations.define("TweetButton.tw_count=none",
    ca = u"Invisible",
    es = u"Invisible",
    en = u"None"
)

translations.define("TweetButton.tw_count=horizontal",
    ca = u"Horitzontal",
    es = u"Horizontal",
    en = u"Horizontal"
)

translations.define("TweetButton.tw_count=vertical",
    ca = u"Vertical",
    es = u"Vertical",
    en = u"Vertical"
)

# FlashBlock
#------------------------------------------------------------------------------
translations.define("FlashBlock",
    ca = u"Animació Flash",
    es = u"Animación Flash",
    en = u"Flash animation"
)

translations.define("FlashBlock-plural",
    ca = u"Animacions Flash",
    es = u"Animaciones Flash",
    en = u"Flash animations"
)

translations.define("FlashBlock.swf_file",
    ca = u"Fitxer Flash",
    es = u"Fichero Flash",
    en = u"Flash file"
)

translations.define("FlashBlock.swf_file",
    ca = u"Fitxer Flash",
    es = u"Fichero Flash",
    en = u"Flash file"
)

translations.define("FlashBlock.width",
    ca = u"Amplada",
    es = u"Ancho",
    en = u"Width"
)

translations.define("FlashBlock.height",
    ca = u"Alçada",
    es = u"Alto",
    en = u"Height"
)

translations.define("FlashBlock.flash_version",
    ca = u"Versió del reproductor Flash",
    es = u"Versión del reproductor Flash",
    en = u"Flash player version"
)

translations.define("FlashBlock.flash_vars",
    ca = u"Variables Flash",
    es = u"Variables Flash",
    en = u"Flash variables"
)

translations.define("FlashBlock.flash_params",
    ca = u"Paràmetres Flash",
    es = u"Parámetros Flash",
    en = u"Flash parameters"
)

translations.define("FlashBlock.flash_attributes",
    ca = u"Atributs Flash",
    es = u"Atributos Flash",
    en = u"Flash attributes"
)

# PublishableListing
#------------------------------------------------------------------------------
translations.define("PublishableListing",
    ca = u"Llistat d'elements publicables",
    es = u"Listado de elementos publicables",
    en = u"Publishable elements listing"
)

translations.define("PublishableListing-plural",
    ca = u"Llistats d'elements publicables",
    es = u"Listados de elementos publicables",
    en = u"Publishable elements listings"
)

translations.define("PublishableListing.listing",
    ca = u"Llistat",
    es = u"Listado",
    en = u"Listing"
)

translations.define("PublishableListing.publishables",
    ca = u"Elements publicables",
    es = u"Elementos publicables",
    en = u"Publishable elements"
)

translations.define("PublishableListing.item_accessibility",
    ca = u"Control d'estat dels elements",
    es = u"Control de estado de los elementos",
    en = u"Item accessibility check"
)

translations.define("PublishableListing.item_accessibility=accessible",
    ca = u"Elements publicats i amb drets de lectura",
    es = u"Elementos publicados y con derechos de lectura",
    en = u"Published items with read privileges"
)

translations.define("PublishableListing.item_accessibility=published",
    ca = u"Elements publicats, tinguin o no drets de lectura",
    es = u"Elementos publicados, tengan o no derechos de lectura",
    en = u"Published items, regardless of read privileges"
)

translations.define("PublishableListing.item_accessibility=any",
    ca = u"Qualsevol element",
    es = u"Cualquier elemento",
    en = u"Any item"
)

translations.define("PublishableListing.listing_order",
    ca = u"Ordenació",
    es = u"Ordenación",
    en = u"Order"
)

translations.define("PublishableListing.listing_order=arbitrary",
    ca = u"Arbitrària",
    es = u"Arbitraria",
    en = u"Arbitrary"
)

translations.define("PublishableListing.listing_order=-last_update_time",
    ca = u"Última modificació",
    es = u"Última modificación",
    en = u"Last update"
)

translations.define("PublishableListing.links_open_in_new_window",
    ca = u"Obrir els enllaços a una nova finestra",
    es = u"Abrir los enlaces en una ventana nueva",
    en = u"Open links in a new window"
)

translations.define("PublishableListing.links_force_download",
    ca = u"Forçar descàrrega",
    es = u"Forzar descarga",
    en = u"Force download"
)

translations.define("PublishableListing.paginated",
    ca = u"Paginar els resultats",
    es = u"Paginar los resultados",
    en = u"Paginate results"
)

translations.define("PublishableListing.page_size",
    ca = u"Mida del llistat",
    es = u"Tamaño del listado",
    en = u"Listing size"
)

translations.define("PublishableListing.view_class",
    ca = u"Aparença",
    es = u"Apariencia",
    en = u"Appearence"
)

translations.define(
    "PublishableListing.view_class=woost.views.PublishableTextualListing",
    ca = u"Només text",
    es = u"Solo texto",
    en = u"Text only"
)

translations.define(
    "PublishableListing.view_class=woost.views.PublishableIconListing",
    ca = u"Icona i text",
    es = u"Icono y texto",
    en = u"Icon and text"
)

translations.define(
    "PublishableListing.view_class=woost.views.PublishableGrid",
    ca = u"Graella",
    es = u"Parrilla",
    en = u"Grid"
)

translations.define(
    "PublishableListing.view_class=woost.views.PublishableCollage",
    ca = u"Collage",
    es = u"Collage",
    en = u"Collage"
)

translations.define("PublishableListing.element_type",
    ca = u"Tipus d'element",
    es = u"Tipo de elemento",
    en = u"Element type"
)

# RichTextEditor
#------------------------------------------------------------------------------
translations.define("woost.views.RichTextEditor.styles_menu_entry",
    ca = u"Estils",
    es = u"Estilos",
    en = u"Styles"
)

# EnabledTranslationsSelector
#------------------------------------------------------------------------------
translations.define(
    "woost.views.EnabledTranslationsSelector.selected_items_panel.heading",
    ca = u"Traduccions actives",
    es = u"Traducciones activas",
    en = u"Enabled translations"
)

translations.define(
    "woost.views.EnabledTranslationsSelector.eligible_items_panel.heading",
    ca = u"Traduccions inactives",
    es = u"Traducciones inactivas",
    en = u"Disabled translations"
)

translations.define(
    "woost.views.EnabledTranslationsSelector.selected_items_panel."
    "toggle_button",
    ca = u"Desactivar",
    es = u"Desactivar",
    en = u"Disable"
)

translations.define(
    "woost.views.EnabledTranslationsSelector.eligible_items_panel."
    "toggle_button",
    ca = u"Activar",
    es = u"Activar",
    en = u"Enable"
)

# woost.views.ChangeLog
#------------------------------------------------------------------------------
translations.define(
    "woost.views.ChangeLog.change_list_grouped_entry.change_targets_display",
    ca = lambda model, count:
        str(count) + u" " + translations(
            model.name + plural2(count, "", "-plural")
        ),
    es = lambda model, count:
        str(count) + u" " + translations(
            model.name + plural2(count, "", "-plural")
        ),
    en = lambda model, count:
        str(count) + u" " + translations(
            model.name + plural2(count, "", "-plural")
        )
)

