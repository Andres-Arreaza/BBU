import React, { useState, useEffect } from "react";
import Swal from "sweetalert2";

const ServidorTabla = ({ obtenerServidorPorId, servidores, setServidores }) => {
    const [paginaActual, setPaginaActual] = useState(1);
    const [servidoresPorPagina, setServidoresPorPagina] = useState(20);

    const handleCantidadCambio = (e) => {
        setServidoresPorPagina(Number(e.target.value));
        setPaginaActual(1);
    };

    // 🔹 Obtener servidores activos desde la API
    const actualizarServidores = async () => {
        try {
            const response = await fetch(`${process.env.BACKEND_URL}/api/servidores`);
            const data = await response.json();
            const servidoresFiltrados = data.filter((servidor) => servidor.activo === true);
            setServidores(servidoresFiltrados);
        } catch (error) {
            console.error("Error al obtener servidores:", error);
        }
    };

    useEffect(() => {
        actualizarServidores();
    }, []);

    const abrirModalLink = (servidor) => {
        if (!servidor || !servidor.link) return;

        Swal.fire({
            title: "Información del Enlace",
            html: `
                <div style="text-align: left;">
                    <p><strong>Servidor:</strong> ${servidor.nombre || "No disponible"}</p>
                    <p><strong>Descripción:</strong> ${servidor.descripcion || "No disponible"}</p>
                    <p><strong>Enlace:</strong> <a href="${servidor.link}" target="_blank" rel="noopener noreferrer">${servidor.link}</a></p>
                </div>
            `,
            showConfirmButton: true,
            confirmButtonText: "Cerrar",
            confirmButtonColor: "#dc3545",
            width: "50%",
            customClass: { title: "swal-title-green" }
        });
    };

    const handleEliminarConfirmacion = (servidor) => {
        Swal.fire({
            title: `¿Seguro que desea eliminar el servidor ${servidor.nombre}?`,
            text: "El servidor será eliminado de forma permanente.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#dc3545",
            cancelButtonColor: "#3349",
            confirmButtonText: "Eliminar",
            cancelButtonText: "Cancelar",
            width: "50%",
            customClass: { title: "swal-title-green" }
        }).then(async (result) => {
            if (result.isConfirmed) {
                await handleBorradoLogico(servidor.id);
                actualizarServidores();
            }
        });
    };

    const handleBorradoLogico = async (id) => {
        try {
            const response = await fetch(`${process.env.BACKEND_URL}/api/servidores/${id}`, {
                method: "DELETE"
            });

            if (response.ok) {
                Swal.fire({
                    title: "Eliminado",
                    text: "El servidor se ha eliminado exitosamente.",
                    icon: "success",
                    timer: 2000,
                    showConfirmButton: false,
                    width: "50%",
                    customClass: { title: "swal-title-green" }
                }).then(() => {
                    actualizarServidores(); // 🔹 Recarga la tabla después de la eliminación
                });
            } else {
                Swal.fire("Error", "No se pudo eliminar el servidor.", "error");
            }
        } catch (error) {
            console.error("Error al actualizar el servidor:", error);
            Swal.fire("Error", "No se pudo conectar con el servidor.", "error");
        }
    };

    const totalPaginas = Math.max(1, Math.ceil(servidores.length / servidoresPorPagina));
    const indiceInicial = (paginaActual - 1) * servidoresPorPagina;
    const indiceFinal = indiceInicial + servidoresPorPagina;
    const servidoresPaginados = servidores.slice(indiceInicial, indiceFinal);

    return (
        <div>
            <div className="cantidad-servidores">
                <span className="servidores-contador">Servidores creados: {servidores.length}</span>
                <label>Servidores por página:</label>
                <select onChange={handleCantidadCambio} value={servidoresPorPagina}>
                    <option value="20">20</option>
                    <option value="30">30</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                    <option value="150">150</option>
                    <option value="200">200</option>
                </select>
            </div>

            <table className="tabla-servidores">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Tipo</th>
                        <th>IP</th>
                        <th>Servicio</th>
                        <th>Capa</th>
                        <th>Ambiente</th>
                        <th>Balanceador</th>
                        <th>VLAN</th>
                        <th>Dominio</th>
                        <th>S.O.</th>
                        <th>Estatus</th>
                        <th>Descripción</th>
                        <th>Link</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {servidoresPaginados.length > 0 ? (
                        servidoresPaginados.map((servidor) => (
                            <tr key={servidor.id}>
                                <td>{servidor.nombre || "Sin nombre"}</td>
                                <td>{servidor.tipo || "Sin tipo"}</td>
                                <td>{servidor.ip || "Sin IP"}</td>
                                <td>{servidor.servicios?.[0]?.nombre || "Sin servicio"}</td>
                                <td>{servidor.capas?.[0]?.nombre || "Sin capa"}</td>
                                <td>{servidor.ambientes?.[0]?.nombre || "Sin ambiente"}</td>
                                <td>{servidor.balanceador || "Sin balanceador"}</td>
                                <td>{servidor.vlan || "Sin VLAN"}</td>
                                <td>{servidor.dominios?.[0]?.nombre || "Sin dominio"}</td>
                                <td>{servidor.sistemasOperativos?.[0]?.nombre || "Sin S.O."}</td>
                                <td>{servidor.estatus?.[0]?.nombre || "Sin estatus"}</td>
                                <td>{servidor.descripcion || "Sin descripción"}</td>
                                <td>
                                    <button className="ver-link-btn icon-btn" onClick={() => abrirModalLink(servidor)}>
                                        <span className="material-symbols-outlined">visibility</span>
                                    </button>
                                </td>
                                <td>
                                    <button className="editar-btn icon-btn" onClick={() => obtenerServidorPorId(servidor.id)}>
                                        <span className="material-icons"><i className="fas fa-edit"></i></span>
                                    </button>
                                    <button className="eliminar-btn icon-btn" onClick={() => handleEliminarConfirmacion(servidor)}>
                                        <span className="material-icons"><i className="fas fa-trash"></i></span>
                                    </button>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="14">No hay servidores disponibles.</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
};

export default ServidorTabla;