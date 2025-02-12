package com.example.myapplication

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.CalendarView
import android.widget.Toast
import androidx.fragment.app.Fragment

class WhiteFrag : Fragment() {
    private var listener: OnDateChangeListener? = null

    // Интерфейс для передачи данных в активность
    interface OnDateChangeListener {
        fun onDateSelected(date: String)
    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        if (context is OnDateChangeListener) {
            listener = context
        } else {
            throw RuntimeException("$context must implement OnDateChangeListener")
        }
    }

    override fun onDetach() {
        super.onDetach()
        listener = null
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_white, container, false)
        val calendarView = view.findViewById<CalendarView>(R.id.calendarViewFr)

        calendarView.setOnDateChangeListener { _, year, month, dayOfMonth ->
            // Создаем строку с выбранной датой
            val selectedDate = "$dayOfMonth.${month + 1}.$year"

            // Показываем Toast с выбранной датой
            Toast.makeText(requireContext(), "Вы выбрали: $selectedDate", Toast.LENGTH_SHORT).show()

            // Передаем дату в активность через интерфейс
            listener?.onDateSelected(selectedDate)
        }

        return view
    }

    companion object {
        @JvmStatic
        fun newInstance() = WhiteFrag()
    }
}