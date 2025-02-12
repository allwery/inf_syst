package com.example.myapplication

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class Authorization : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main2)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets

        }
        val userLogin=findViewById<EditText>(R.id.userLoginAuth)
        val userPassword=findViewById<EditText>(R.id.userPassAuth)
        val button=findViewById<Button>(R.id.buttonAuth)
        button.setOnClickListener {
            val login=userLogin.text.toString().trim()
            val pass=userPassword.text.toString().trim()

            if(login=="" ||pass=="" ){
                Toast.makeText(this,"Пусто чет", Toast.LENGTH_LONG).show()
            }
            else{
                val db=DBHelper(this,null)
                val isAuth=db.getUser(login,pass)
                if(isAuth){
                    Toast.makeText(this,"Пользователь $login авторизован ", Toast.LENGTH_LONG).show()
                    userLogin.text.clear()
                    userPassword.text.clear()
                    val intent= Intent(this,ItemsActivity::class.java)
                    startActivity(intent)
                }else{
                    Toast.makeText(this,"Пользователь $login не авторизован ", Toast.LENGTH_LONG).show()
                }


            }
        }
    }
}